"""Prompt manager selector for choosing provider implementation."""

from libs.base.selector import BaseToolSelector


class PromptManagerSelector(BaseToolSelector):
    """Selector for prompt manager providers.

    Provides factory method to create prompt manager clients.

    Available providers:
        - langfuse: Langfuse prompt management

    Example:
        >>> from libs.llm.prompt_manager.selector import PromptManagerSelector
        >>>
        >>> pm = PromptManagerSelector.create(
        ...     provider="langfuse",
        ...     public_key="pk-lf-...",
        ...     secret_key="sk-lf-..."
        ... )
        >>>
        >>> prompt = pm.get_prompt("triage_classifier")
        >>> compiled = prompt.compile(ticket_content="...")
    """

    _PROVIDERS = {
        "langfuse": "libs.llm.prompt_manager.langfuse.main.LangfusePromptManager",
    }
