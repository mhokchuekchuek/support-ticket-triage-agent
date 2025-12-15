"""Ticket matcher agent for matching messages to existing tickets."""

import json
from typing import Any, Optional, List

from langchain_core.messages import HumanMessage, SystemMessage

from src.modules.agents.base import BaseAgent
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class TicketMatcherAgent(BaseAgent):
    """Agent that matches new messages to existing active tickets.

    Uses LLM to analyze if a new customer message relates to any
    existing active ticket in Redis. This enables multi-turn
    conversations and proper ticket routing.

    System prompt is loaded from Langfuse prompt manager.

    Attributes:
        name: Agent name.
        llm: LangChain-compatible LLM.
        observability: Observability wrapper for tracing.
        prompt_manager: Prompt manager for loading prompts.
    """

    AGENT_NAME = "ticket_matcher"

    def __init__(
        self,
        llm,
        observability: Optional[Any] = None,
        prompt_manager: Optional[Any] = None,
        agent_config: Optional[dict] = None,
    ):
        """Initialize ticket matcher agent.

        Args:
            llm: LangChain-compatible LLM.
            observability: Observability wrapper for tracing.
            prompt_manager: Prompt manager for loading prompts.
            agent_config: Agent configuration with prompt settings.
        """
        super().__init__(name=self.AGENT_NAME)
        self.llm = llm
        self.observability = observability
        self.prompt_manager = prompt_manager
        self.agent_config = agent_config or {}
        self.prompt_config = self.agent_config.get("prompt", {})

        # Load prompt from prompt manager
        self.system_prompt = None
        if self.prompt_manager and self.prompt_config:
            try:
                prompt_id = self.prompt_config.get("id", "triage_ticket_matcher")
                prompt_label = self.prompt_config.get("environment", "production")

                self.logger.info(
                    f"Fetching ticket matcher prompt from Langfuse: "
                    f"name={prompt_id}, label={prompt_label}"
                )

                prompt_obj = self.prompt_manager.get_prompt(
                    name=prompt_id,
                    label=prompt_label,
                )
                self.system_prompt = prompt_obj.prompt
                self.logger.info("Ticket matcher prompt loaded from Langfuse")

            except Exception as e:
                self.logger.warning(f"Failed to load prompt from Langfuse: {e}")

        self.logger.info("TicketMatcherAgent initialized")

    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Match new message to existing tickets.

        Args:
            state: State containing new_message and active_tickets.

        Returns:
            Updated state with match_result.
        """
        new_message = state.get("new_message", "")
        active_tickets = state.get("active_tickets", [])

        self.logger.info(f"Matching message against {len(active_tickets)} active tickets")

        state["current_agent"] = self.name

        # If no active tickets, no matching needed
        if not active_tickets:
            self.logger.info("No active tickets to match against")
            state["match_result"] = {
                "matched_ticket_id": None,
                "confidence": "high",
                "reasoning": "No active tickets found for this customer",
            }
            return state

        try:
            # Build user prompt with ticket summaries
            user_prompt = self._build_user_prompt(new_message, active_tickets)

            # Call LLM
            messages = []
            if self.system_prompt:
                messages.append(SystemMessage(content=self.system_prompt))
            messages.append(HumanMessage(content=user_prompt))
            response = self.llm.invoke(messages)

            # Parse response
            match_result = self._parse_response(response.content)
            state["match_result"] = match_result

            # Log to observability
            if self.observability:
                try:
                    self.observability.trace_generation(
                        name="ticket_matcher",
                        input_data={"message": new_message[:100], "ticket_count": len(active_tickets)},
                        output=match_result,
                        model=str(getattr(self.llm, "model_name", "unknown")),
                    )
                except Exception as e:
                    self.logger.warning(f"Failed to trace ticket matcher: {e}")

            self.logger.info(
                f"Match result: ticket={match_result.get('matched_ticket_id')}, "
                f"confidence={match_result.get('confidence')}"
            )

        except Exception as e:
            self.logger.error(f"Ticket matching failed: {e}", exc_info=True)
            state["match_result"] = {
                "matched_ticket_id": None,
                "confidence": "low",
                "reasoning": f"Matching failed: {str(e)}",
            }

        return state

    def _build_user_prompt(self, new_message: str, active_tickets: List[dict]) -> str:
        """Build user prompt with message and ticket summaries.

        Args:
            new_message: New customer message.
            active_tickets: List of active ticket dictionaries.

        Returns:
            Formatted user prompt.
        """
        tickets_text = "\n".join(
            f"- **{t.get('ticket_id', 'unknown')}**: {t.get('summary', 'No summary')}"
            for t in active_tickets
        )

        return f"""## New Customer Message
{new_message}

## Active Tickets
{tickets_text}

Analyze if the new message relates to any active ticket."""

    def _parse_response(self, response: str) -> dict:
        """Parse LLM response into match result.

        Args:
            response: Raw LLM response.

        Returns:
            Parsed match result dictionary.
        """
        try:
            # Extract JSON from response
            json_str = response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0]

            data = json.loads(json_str.strip())

            return {
                "matched_ticket_id": data.get("matched_ticket_id"),
                "confidence": data.get("confidence", "low"),
                "reasoning": data.get("reasoning", ""),
            }

        except (json.JSONDecodeError, KeyError) as e:
            self.logger.error(f"Failed to parse matcher response: {e}")
            return {
                "matched_ticket_id": None,
                "confidence": "low",
                "reasoning": f"Parse failed: {response[:100]}",
            }
