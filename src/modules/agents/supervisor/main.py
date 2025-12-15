"""Supervisor agent for ticket classification and routing."""

import json
from typing import List, Optional

from langchain.agents import create_agent
from langchain.tools import BaseTool
from langchain_core.messages import HumanMessage, SystemMessage

from src.modules.agents.base import BaseAgent
from src.modules.graph.state import AgentState, SupervisorDecision, TicketType
from src.entities.triage_result import UrgencyLevel
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class SupervisorAgent(BaseAgent):
    """Supervisor agent for classifying and routing tickets.

    Uses customer_lookup tool to get customer context, then classifies
    urgency level and ticket type to route to the appropriate specialist.

    System prompt is loaded from Langfuse prompt manager.

    Attributes:
        llm: LangChain-compatible LLM.
        tools: List of tools (customer_lookup).
        observability: Observability wrapper for tracing.
        prompt_manager: Prompt manager for loading prompts.
        agent_config: Agent configuration including prompt settings.
        agent: ReAct agent executor.
    """

    def __init__(
        self,
        llm,
        tools: List[BaseTool],
        observability: Optional[any] = None,
        prompt_manager: Optional[any] = None,
        agent_config: Optional[dict] = None,
    ):
        """Initialize supervisor agent.

        Args:
            llm: LangChain-compatible LLM.
            tools: List of tools (customer_lookup).
            observability: Observability wrapper for tracing.
            prompt_manager: Prompt manager for loading prompts.
            agent_config: Agent configuration with prompt settings.
        """
        super().__init__("SupervisorAgent")
        self.llm = llm
        self.tools = tools
        self.observability = observability
        self.prompt_manager = prompt_manager
        self.agent_config = agent_config or {}
        self.prompt_config = self.agent_config.get("prompt", {})

        # Load prompt from prompt manager
        system_prompt = None
        if self.prompt_manager and self.prompt_config:
            try:
                prompt_id = self.prompt_config.get("id", "triage_supervisor")
                prompt_label = self.prompt_config.get("environment", "production")

                self.logger.info(
                    f"Fetching supervisor prompt from Langfuse: "
                    f"name={prompt_id}, label={prompt_label}"
                )

                prompt_obj = self.prompt_manager.get_prompt(
                    name=prompt_id,
                    label=prompt_label,
                )
                system_prompt = prompt_obj.prompt
                self.logger.info("Supervisor prompt loaded from Langfuse")

            except Exception as e:
                self.logger.warning(f"Failed to load prompt from Langfuse: {e}")

        # Store system prompt for use in execute
        self.system_prompt = system_prompt

        # Create agent with tools
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
        )
        self.logger.info(f"SupervisorAgent initialized with {len(tools)} tools")

    def execute(self, state: AgentState) -> AgentState:
        """Classify ticket and decide routing.

        Args:
            state: Current agent state with ticket and translation info.

        Returns:
            Updated state with supervisor decision.
        """
        ticket = state["ticket"]
        translation = state.get("translation")

        self.logger.info(f"Classifying ticket: {ticket.ticket_id}")

        state["current_agent"] = self.name
        state["iteration"] = state.get("iteration", 0) + 1

        try:
            # Build input prompt with translated content if available
            ticket_content = self._build_ticket_content(ticket, translation)

            user_prompt = f"""Analyze and classify this support ticket.

{ticket_content}

Use the customer_lookup tool to get additional customer context.
Then classify the urgency and ticket type.

Return your classification as JSON."""

            # Invoke agent with messages
            messages = []
            if self.system_prompt:
                messages.append(SystemMessage(content=self.system_prompt))
            messages.append(HumanMessage(content=user_prompt))
            result = self.agent.invoke({"messages": messages})

            # Get final output from last message
            final_output = result["messages"][-1].content

            # Parse supervisor decision
            decision = self._parse_decision(final_output)
            state["supervisor_decision"] = decision

            # Log to Langfuse
            if self.observability:
                try:
                    self.observability.trace_generation(
                        name="supervisor",
                        input_data={"ticket_id": ticket.ticket_id},
                        output=decision.model_dump(),
                        model=str(getattr(self.llm, "model_name", "unknown")),
                        session_id=ticket.ticket_id,
                    )
                except Exception as e:
                    self.logger.warning(f"Failed to trace supervisor: {e}")

            self.logger.info(
                f"Supervisor decision: urgency={decision.urgency.value}, "
                f"type={decision.ticket_type.value}, "
                f"escalate={decision.requires_escalation}"
            )

        except Exception as e:
            self.logger.error(f"Supervisor classification failed: {e}", exc_info=True)
            # Fallback decision
            state["supervisor_decision"] = SupervisorDecision(
                urgency=UrgencyLevel.MEDIUM,
                ticket_type=TicketType.GENERAL,
                reasoning=f"Classification failed: {str(e)}",
                requires_escalation=False,
            )

        return state

    def _build_ticket_content(self, ticket, translation) -> str:
        """Build ticket content string, using translation if available.

        Args:
            ticket: Original ticket.
            translation: Translation result if ticket was non-English.

        Returns:
            Formatted ticket content string.
        """
        # Use translated messages if available
        if translation and not translation.is_english and translation.translated_messages:
            messages_text = "\n".join(
                f"[{ticket.messages[i].role}] ({ticket.messages[i].timestamp}): {msg}"
                for i, msg in enumerate(translation.translated_messages)
            )
            language_note = f"**Original Language:** {translation.original_language}\n"
        else:
            messages_text = "\n".join(
                f"[{msg.role}] ({msg.timestamp}): {msg.content}"
                for msg in ticket.messages
            )
            language_note = ""

        return f"""## Ticket Information
- **Ticket ID:** {ticket.ticket_id}
- **Customer ID:** {ticket.customer_id}
{language_note}
## Customer Context (from ticket)
- **Plan:** {ticket.customer_info.plan}
- **Tenure:** {ticket.customer_info.tenure_months} months
- **Region:** {ticket.customer_info.region or 'N/A'}
- **Seats:** {ticket.customer_info.seats or 'N/A'}
- **Previous Tickets:** {ticket.customer_info.previous_tickets}

## Conversation
{messages_text}"""

    def _parse_decision(self, output: str) -> SupervisorDecision:
        """Parse agent output into SupervisorDecision.

        Args:
            output: Raw agent output text.

        Returns:
            Parsed SupervisorDecision.
        """
        try:
            # Extract JSON from output
            json_str = output
            if "```json" in output:
                json_str = output.split("```json")[1].split("```")[0]
            elif "```" in output:
                json_str = output.split("```")[1].split("```")[0]

            data = json.loads(json_str.strip())

            # Map urgency string to enum
            urgency_str = data.get("urgency", "medium").lower()
            urgency = UrgencyLevel(urgency_str)

            # Map ticket type string to enum
            type_str = data.get("ticket_type", "general").lower()
            ticket_type = TicketType(type_str)

            return SupervisorDecision(
                urgency=urgency,
                ticket_type=ticket_type,
                reasoning=data.get("reasoning", ""),
                requires_escalation=data.get("requires_escalation", False),
            )

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            self.logger.error(f"Failed to parse supervisor output: {e}")
            # Fallback
            return SupervisorDecision(
                urgency=UrgencyLevel.MEDIUM,
                ticket_type=TicketType.GENERAL,
                reasoning=f"Parse failed: {output[:200]}",
                requires_escalation=False,
            )
