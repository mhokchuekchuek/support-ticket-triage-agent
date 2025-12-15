"""Base class for specialist agents (billing, technical, general)."""

import json
from typing import List, Optional

from langchain.agents import create_agent
from langchain.tools import BaseTool
from langchain_core.messages import HumanMessage, SystemMessage

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


class SpecialistBaseAgent(BaseAgent):
    """Base class for specialist agents.

    Provides shared functionality for billing, technical, and general agents:
    - Prompt loading from Langfuse
    - ReAct agent creation with kb_search tool
    - Response parsing into TriageResult

    Subclasses should set:
    - AGENT_NAME: Name for logging and identification
    - PROMPT_ID: Default Langfuse prompt ID
    - DOMAIN: Domain category (billing, technical, general)

    Attributes:
        llm: LangChain-compatible LLM.
        tools: List of tools (kb_search).
        observability: Observability wrapper for tracing.
        prompt_manager: Prompt manager for loading prompts.
        agent_config: Agent configuration including prompt settings.
        agent: ReAct agent executor.
        prompt_obj: Langfuse prompt object for compilation.
    """

    AGENT_NAME: str = "SpecialistAgent"
    PROMPT_ID: str = "triage_specialist"
    DOMAIN: str = "general"

    def __init__(
        self,
        llm,
        tools: List[BaseTool],
        observability: Optional[any] = None,
        prompt_manager: Optional[any] = None,
        agent_config: Optional[dict] = None,
    ):
        """Initialize specialist agent.

        Args:
            llm: LangChain-compatible LLM.
            tools: List of tools (kb_search).
            observability: Observability wrapper for tracing.
            prompt_manager: Prompt manager for loading prompts.
            agent_config: Agent configuration with prompt settings.
        """
        super().__init__(self.AGENT_NAME)
        self.llm = llm
        self.tools = tools
        self.observability = observability
        self.prompt_manager = prompt_manager
        self.agent_config = agent_config or {}
        self.prompt_config = self.agent_config.get("prompt", {})

        # Load prompt object from prompt manager
        self.prompt_obj = self._load_prompt()

        # Create agent with tools
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
        )
        self.logger.info(f"{self.AGENT_NAME} initialized with {len(tools)} tools")

    def _load_prompt(self):
        """Load prompt object from prompt manager.

        Returns:
            Langfuse prompt object with compile() method, or None if unavailable.
        """
        if not self.prompt_manager:
            self.logger.warning(f"No prompt manager for {self.AGENT_NAME}")
            return None

        prompt_id = self.prompt_config.get("id", self.PROMPT_ID)
        prompt_label = self.prompt_config.get("environment", "production")

        self.logger.info(
            f"Fetching {self.AGENT_NAME} prompt from Langfuse: "
            f"name={prompt_id}, label={prompt_label}"
        )

        try:
            prompt_obj = self.prompt_manager.get_prompt(
                name=prompt_id,
                label=prompt_label,
            )
            self.logger.info(f"{self.AGENT_NAME} prompt loaded from Langfuse")
            return prompt_obj
        except Exception as e:
            self.logger.warning(f"Failed to load prompt from Langfuse: {e}")
            return None

    def execute(self, state: AgentState) -> AgentState:
        """Execute specialist triage.

        Args:
            state: Current agent state with ticket, translation, and supervisor decision.

        Returns:
            Updated state with triage result.
        """
        ticket = state["ticket"]
        translation = state.get("translation")
        supervisor_decision = state.get("supervisor_decision")

        self.logger.info(f"{self.AGENT_NAME} processing ticket: {ticket.ticket_id}")

        state["current_agent"] = self.name
        state["iteration"] = state.get("iteration", 0) + 1

        # Compile prompt with ticket data
        compiled_prompt = self._compile_prompt(ticket, translation, supervisor_decision)

        # Invoke agent with messages
        messages = [
            SystemMessage(content=compiled_prompt),
            HumanMessage(content="Please analyze this ticket and provide your triage result as JSON."),
        ]
        result = self.agent.invoke({"messages": messages})

        # Get final output from last message
        final_output = result["messages"][-1].content

        # Parse triage result
        triage_result = self._parse_triage_result(final_output, supervisor_decision, translation)
        state["triage_result"] = triage_result

        # Log to Langfuse
        if self.observability:
            try:
                self.observability.trace_generation(
                    name=self.AGENT_NAME.lower(),
                    input_data={"ticket_id": ticket.ticket_id},
                    output=triage_result.model_dump(),
                    model=str(getattr(self.llm, "model_name", "unknown")),
                    session_id=ticket.ticket_id,
                )
            except Exception as e:
                self.logger.warning(f"Failed to trace {self.AGENT_NAME}: {e}")

        self.logger.info(
            f"{self.AGENT_NAME} result: urgency={triage_result.urgency.value}, "
            f"action={triage_result.recommended_action.value}"
        )

        return state

    def _compile_prompt(self, ticket, translation, supervisor_decision) -> str:
        """Compile Langfuse prompt with ticket variables.

        Args:
            ticket: Original ticket.
            translation: Translation result.
            supervisor_decision: Supervisor's classification.

        Returns:
            Compiled prompt string.
        """
        # Build ticket content
        if translation and not translation.is_english and translation.translated_messages:
            messages_text = "\n".join(
                f"[{ticket.messages[i].role}] ({ticket.messages[i].timestamp}): {msg}"
                for i, msg in enumerate(translation.translated_messages)
            )
        else:
            messages_text = "\n".join(
                f"[{msg.role}] ({msg.timestamp}): {msg.content}"
                for msg in ticket.messages
            )

        # Build customer info
        customer_info = (
            f"Plan: {ticket.customer_info.plan}, "
            f"Tenure: {ticket.customer_info.tenure_months} months, "
            f"Region: {ticket.customer_info.region or 'N/A'}, "
            f"Seats: {ticket.customer_info.seats or 'N/A'}, "
            f"Previous Tickets: {ticket.customer_info.previous_tickets}"
        )

        # Get urgency and reasoning
        urgency = supervisor_decision.urgency.value if supervisor_decision else "medium"
        supervisor_reasoning = supervisor_decision.reasoning if supervisor_decision else ""

        # Get original language
        original_language = translation.original_language if translation else "en"

        # Compile prompt using Langfuse prompt object
        return self.prompt_obj.compile(
            ticket_content=messages_text,
            customer_info=customer_info,
            urgency=urgency,
            supervisor_reasoning=supervisor_reasoning,
            original_language=original_language,
        )

    def _parse_triage_result(
        self,
        output: str,
        supervisor_decision,
        translation,
    ) -> TriageResult:
        """Parse agent output into TriageResult.

        Args:
            output: Raw agent output text.
            supervisor_decision: Supervisor's classification.
            translation: Translation result.

        Returns:
            Parsed TriageResult.
        """
        # Extract JSON from output
        json_str = output
        if "```json" in output:
            json_str = output.split("```json")[1].split("```")[0]
        elif "```" in output:
            json_str = output.split("```")[1].split("```")[0]

        data = json.loads(json_str.strip())

        # Map urgency
        urgency_str = data.get("urgency", "medium").lower()
        urgency = UrgencyLevel(urgency_str)

        # Map action
        action_str = data.get("recommended_action", "route_specialist").lower()
        action = RecommendedAction(action_str)

        # Build extracted info
        extracted_data = data.get("extracted_info", {})
        language = translation.original_language if translation else "en"

        extracted_info = ExtractedInfo(
            product_area=extracted_data.get("product_area", self.DOMAIN),
            issue_type=extracted_data.get("issue_type", "unknown"),
            sentiment=extracted_data.get("sentiment", "neutral"),
            language=extracted_data.get("language", language),
        )

        # Build relevant articles
        articles = []
        for article in data.get("relevant_articles", []):
            articles.append(
                RelevantArticle(
                    id=article.get("id", "unknown"),
                    title=article.get("title", "Unknown"),
                    relevance_score=float(article.get("relevance_score", 0.5)),
                )
            )

        return TriageResult(
            urgency=urgency,
            extracted_info=extracted_info,
            recommended_action=action,
            suggested_response=data.get("suggested_response"),
            relevant_articles=articles,
            reasoning=data.get("reasoning", ""),
        )
