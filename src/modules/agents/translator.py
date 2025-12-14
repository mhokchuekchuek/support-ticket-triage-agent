"""Translator agent for language detection and translation."""

import json
from typing import Optional

from langchain_core.messages import HumanMessage, SystemMessage

from src.modules.agents.base import BaseAgent
from src.modules.graph.state import AgentState, TranslationResult
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class TranslatorAgent(BaseAgent):
    """Agent for detecting language and translating non-English tickets.

    This agent runs first in the workflow to ensure all downstream agents
    work with English text while preserving original messages for response generation.

    System prompt is loaded from Langfuse prompt manager.

    Attributes:
        llm: LangChain-compatible LLM for translation.
        observability: Observability wrapper for tracing.
        prompt_manager: Prompt manager for loading prompts.
        agent_config: Agent configuration including prompt settings.
        system_prompt: System prompt loaded from Langfuse.
    """

    def __init__(
        self,
        llm,
        observability: Optional[any] = None,
        prompt_manager: Optional[any] = None,
        agent_config: Optional[dict] = None,
    ):
        """Initialize translator agent.

        Args:
            llm: LangChain-compatible LLM for translation.
            observability: Observability wrapper for tracing.
            prompt_manager: Prompt manager for loading prompts.
            agent_config: Agent configuration with prompt settings.
        """
        super().__init__("TranslatorAgent")
        self.llm = llm
        self.observability = observability
        self.prompt_manager = prompt_manager
        self.agent_config = agent_config or {}
        self.prompt_config = self.agent_config.get("prompt", {})

        # Load prompt from prompt manager
        self.system_prompt = None
        if self.prompt_manager and self.prompt_config:
            try:
                prompt_id = self.prompt_config.get("id", "triage_translator")
                prompt_label = self.prompt_config.get("environment", "production")

                self.logger.info(
                    f"Fetching translator prompt from Langfuse: "
                    f"name={prompt_id}, label={prompt_label}"
                )

                prompt_obj = self.prompt_manager.get_prompt(
                    name=prompt_id,
                    label=prompt_label,
                )
                self.system_prompt = prompt_obj.prompt
                self.logger.info("Translator prompt loaded from Langfuse")

            except Exception as e:
                self.logger.warning(f"Failed to load prompt from Langfuse: {e}")

        self.logger.info("TranslatorAgent initialized")

    def execute(self, state: AgentState) -> AgentState:
        """Detect language and translate if needed.

        Args:
            state: Current agent state with ticket info.

        Returns:
            Updated state with translation result.
        """
        ticket = state["ticket"]
        self.logger.info(f"Detecting language for ticket: {ticket.ticket_id}")

        state["current_agent"] = self.name
        state["iteration"] = state.get("iteration", 0) + 1

        try:
            # Extract message contents
            original_messages = [msg.content for msg in ticket.messages]

            # Build user prompt with ticket content
            messages_text = "\n".join(
                f"Message {i+1}: {content}"
                for i, content in enumerate(original_messages)
            )

            user_prompt = f"""Analyze the following customer support messages:

{messages_text}

Detect the language and translate to English if needed. Return JSON only."""

            # Build messages for LLM
            messages = []
            if self.system_prompt:
                messages.append(SystemMessage(content=self.system_prompt))
            messages.append(HumanMessage(content=user_prompt))

            # Invoke LLM for translation
            response = self.llm.invoke(messages)
            response_text = response.content if hasattr(response, "content") else str(response)

            # Parse response into TranslationResult
            translation_result = self._parse_response(response_text, original_messages)
            state["translation"] = translation_result

            # Log to Langfuse for observability
            if self.observability:
                try:
                    self.observability.trace_generation(
                        name="translator",
                        input_data={"messages": original_messages},
                        output=translation_result.model_dump(),
                        model=str(getattr(self.llm, "model_name", "unknown")),
                        session_id=ticket.ticket_id,
                    )
                except Exception as e:
                    self.logger.warning(f"Failed to trace translation: {e}")

            self.logger.info(
                f"Language detected: {translation_result.original_language}, "
                f"is_english: {translation_result.is_english}"
            )

        except Exception as e:
            self.logger.error(f"Translation failed: {e}", exc_info=True)
            # Fallback: assume English and continue
            state["translation"] = TranslationResult(
                original_language="en",
                is_english=True,
                translated_messages=None,
                original_messages=[msg.content for msg in ticket.messages],
            )

        return state

    def _parse_response(
        self, response: str, original_messages: list[str]
    ) -> TranslationResult:
        """Parse LLM response into TranslationResult.

        Args:
            response: Raw LLM response text.
            original_messages: Original message contents for fallback.

        Returns:
            Parsed TranslationResult.
        """
        try:
            # Extract JSON from response (handle markdown code blocks)
            json_str = response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0]

            data = json.loads(json_str.strip())

            return TranslationResult(
                original_language=data.get("original_language", "en"),
                is_english=data.get("is_english", True),
                translated_messages=data.get("translated_messages"),
                original_messages=data.get("original_messages", original_messages),
            )

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            self.logger.error(f"Failed to parse translation response: {e}")
            # Fallback to English assumption
            return TranslationResult(
                original_language="en",
                is_english=True,
                translated_messages=None,
                original_messages=original_messages,
            )
