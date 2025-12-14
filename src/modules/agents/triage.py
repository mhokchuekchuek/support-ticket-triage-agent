"""Triage agent using ReAct pattern for autonomous tool selection."""
import json
from typing import List, Optional

from langchain.agents import create_agent
from langchain.tools import BaseTool
from langchain_core.messages import AIMessage, HumanMessage

from src.modules.agents.base import BaseAgent
from src.modules.graph.state import AgentState
from src.entities.triage_result import (
    TriageResult,
    UrgencyLevel,
    RecommendedAction,
    ExtractedInfo,
    RelevantArticle,
)
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class TriageAgent(BaseAgent):
    """Triage agent using ReAct pattern for autonomous tool selection.

    Uses LangChain create_agent (ReAct pattern) with tools for:
    - Knowledge base search
    - Customer lookup

    System prompt loaded from prompt manager (Langfuse).
    """

    def __init__(
        self,
        llm,
        tools: List[BaseTool],
        langfuse_client: Optional[any] = None,
        agent_config: Optional[dict] = None,
    ):
        """Initialize triage agent.

        Args:
            llm: LangChain-compatible model (e.g., ChatOpenAI)
            tools: List of tools (KBRetrievalTool, CustomerLookupTool)
            langfuse_client: Optional Langfuse client for observability and prompt
            agent_config: Optional agent configuration (name, prompt, max_history)
        """
        super().__init__("TriageAgent")
        self.llm = llm
        self.tools = tools
        self.langfuse_client = langfuse_client
        self.agent_config = agent_config or {}
        self.agent_name = self.agent_config.get("name", "triage")
        self.prompt_config = self.agent_config.get("prompt", {})

        system_prompt = None
        if self.langfuse_client and self.prompt_config:
            try:
                prompt_id = self.prompt_config.get("id", "agent_triage")
                prompt_version = self.prompt_config.get("version")
                prompt_env = self.prompt_config.get("environment", "dev")

                logger.info(f"Fetching triage prompt from Langfuse: name={prompt_id}, label={prompt_env}")

                prompt_obj = self.langfuse_client.get_prompt(
                    name=prompt_id,
                    version=prompt_version,
                    label=prompt_env
                )
                system_prompt = prompt_obj.prompt
                logger.info("Triage prompt loaded from Langfuse")
            except Exception as e:
                logger.warning(f"Failed to load prompt from Langfuse: {e}")

        self.agent = create_agent(
            model=llm,
            tools=tools,
            prompt=system_prompt,
        )
        logger.info(f"TriageAgent initialized with ReAct pattern ({len(tools)} tools)")

    def execute(self, state: AgentState) -> AgentState:
        """Execute triage with ReAct loop.

        Args:
            state: Current agent state with ticket info

        Returns:
            Updated state with triage result
        """
        try:
            ticket = state["ticket"]
            logger.info(f"Starting triage for ticket: {ticket.ticket_id}")

            state["iteration"] = state.get("iteration", 0) + 1

            user_prompt = self._build_user_prompt(ticket)

            max_history = self.agent_config.get("max_history", 10)
            messages = state["messages"][-max_history:] if len(state["messages"]) > max_history else state["messages"]

            messages_to_send = list(messages) + [HumanMessage(content=user_prompt)]

            result = self.agent.invoke({"messages": messages_to_send})

            logger.debug(f"Agent returned {len(result['messages'])} messages")

            tool_history = []
            for msg in result["messages"]:
                if hasattr(msg, 'tool_calls') and msg.tool_calls:
                    for tool_call in msg.tool_calls:
                        tool_name = tool_call.get('name', 'unknown')
                        if tool_name not in tool_history:
                            tool_history.append(tool_name)
                            logger.debug(f"Tool used: {tool_name}")

            final_output = result["messages"][-1].content

            if self.langfuse_client:
                try:
                    self.langfuse_client.trace_generation(
                        name=self.agent_name,
                        input_data={"ticket_id": ticket.ticket_id, "prompt": user_prompt},
                        output=final_output,
                        model=str(getattr(self.llm, 'model_name', 'unknown')),
                        metadata={"tools_used": tool_history},
                        session_id=ticket.ticket_id,
                    )
                except Exception as e:
                    logger.warning(f"Failed to trace: {e}")

            triage_result = self._parse_response(final_output)
            state["triage_result"] = triage_result

            final_ai_message = None
            for msg in reversed(result["messages"]):
                if isinstance(msg, AIMessage):
                    if not (hasattr(msg, 'tool_calls') and msg.tool_calls):
                        final_ai_message = msg
                        break

            if final_ai_message:
                state["messages"].append(final_ai_message)

            logger.info(
                f"Triage complete: urgency={triage_result.urgency.value}, "
                f"action={triage_result.recommended_action.value}, "
                f"tools_used={tool_history}"
            )

        except Exception as e:
            logger.error(f"Triage failed: {e}", exc_info=True)
            state["triage_result"] = TriageResult(
                urgency=UrgencyLevel.MEDIUM,
                extracted_info=ExtractedInfo(
                    issue_type="unknown",
                    sentiment="neutral",
                ),
                recommended_action=RecommendedAction.ESCALATE_HUMAN,
                reasoning=f"Triage failed: {str(e)}",
            )

        return state

    def _build_user_prompt(self, ticket) -> str:
        """Build user prompt with ticket information."""
        messages_text = "\n".join(
            f"[{msg.role}] ({msg.timestamp}): {msg.content}"
            for msg in ticket.messages
        )

        return f"""## Ticket Information
- **Ticket ID:** {ticket.ticket_id}
- **Customer ID:** {ticket.customer_id}
- **Plan:** {ticket.customer_info.plan}
- **Tenure:** {ticket.customer_info.tenure_months} months
- **Region:** {ticket.customer_info.region or 'N/A'}
- **Seats:** {ticket.customer_info.seats or 'N/A'}
- **Previous Tickets:** {ticket.customer_info.previous_tickets}

## Conversation
{messages_text}"""

    def _parse_response(self, response: str) -> TriageResult:
        """Parse LLM response into TriageResult."""
        try:
            json_str = response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0]

            data = json.loads(json_str.strip())

            return TriageResult(
                urgency=UrgencyLevel(data["urgency"]),
                extracted_info=ExtractedInfo(**data["extracted_info"]),
                recommended_action=RecommendedAction(data["recommended_action"]),
                suggested_response=data.get("suggested_response"),
                relevant_articles=[
                    RelevantArticle(**a) for a in data.get("relevant_articles", [])
                ],
                reasoning=data["reasoning"],
            )
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(f"Failed to parse response: {e}")
            return TriageResult(
                urgency=UrgencyLevel.MEDIUM,
                extracted_info=ExtractedInfo(
                    issue_type="unknown",
                    sentiment="neutral",
                ),
                recommended_action=RecommendedAction.ESCALATE_HUMAN,
                reasoning=f"Failed to parse LLM response: {str(e)}",
            )
