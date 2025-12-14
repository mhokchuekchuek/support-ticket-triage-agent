"""Observability tool selector for choosing provider implementation."""

from libs.base.selector import BaseToolSelector


class ObservabilitySelector(BaseToolSelector):
    """Selector for observability tool providers.

    Provides factory method to create observability clients for LLM tracing.

    Available providers:
        - langfuse: Langfuse client for LLM tracing with LangChain CallbackHandler

    Example:
        >>> from libs.llm.observability.selector import ObservabilitySelector
        >>>
        >>> # Create Langfuse observability client
        >>> obs = ObservabilitySelector.create(
        ...     provider="langfuse",
        ...     public_key="pk-lf-...",
        ...     secret_key="sk-lf-...",
        ...     host="https://cloud.langfuse.com"
        ... )
        >>>
        >>> # Get callback handler for LangGraph automatic tracing
        >>> handler = obs.get_callback_handler(session_id="ticket-123")
        >>> result = agent.invoke(input, config={"callbacks": [handler]})
        >>>
        >>> # Flush traces after request
        >>> obs.flush()
    """

    _PROVIDERS = {
        "langfuse": "libs.llm.observability.langfuse.main.LangfuseObservability",
    }
