"""LLM client selector for choosing provider implementation."""

from libs.base.selector import BaseToolSelector


class LLMClientSelector(BaseToolSelector):
    """Selector for LLM client providers.

    Available providers:
        - litellm: LiteLLM proxy client (HTTP-based)
        - langchain: LangChain ChatOpenAI wrapper for LiteLLM proxy

    Example:
        >>> from libs.llm.client.selector import LLMClientSelector
        >>>
        >>> # LiteLLM (for direct API use, RAG)
        >>> client = LLMClientSelector.create(
        ...     provider="litellm",
        ...     proxy_url="http://litellm-proxy:4000",
        ...     completion_model="gpt-4o-mini"
        ... )
        >>> response = client.generate(prompt="Hello")
        >>>
        >>> # LangChain (for agents, chains)
        >>> client = LLMClientSelector.create(
        ...     provider="langchain",
        ...     proxy_url="http://litellm-proxy:4000"
        ... )
        >>> chat = client.get_client(model="gpt-4")
    """

    _PROVIDERS = {
        "litellm": "libs.llm.client.litellm.main.LLMClient",
        "langchain": "libs.llm.client.langchain.main.LLMClient",
    }
