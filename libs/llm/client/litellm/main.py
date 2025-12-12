"""LiteLLM proxy client using HTTP requests.

The LiteLLM proxy exposes OpenAI-compatible endpoints.
We use httpx to make direct HTTP calls to the proxy.

Reference: https://docs.litellm.ai/docs/proxy/quick_start
"""

from typing import Optional

import httpx

from libs.llm.client.base import BaseLLM
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class LLMClient(BaseLLM):
    """LiteLLM proxy client using HTTP requests.

    The proxy exposes OpenAI-compatible /chat/completions and /embeddings endpoints.
    We use httpx to make direct HTTP calls.

    The proxy provides:
    - Automatic caching via Redis
    - Multi-provider support (Claude, GPT-4, etc.)
    - Load balancing and fallbacks

    Reference: https://docs.litellm.ai/docs/proxy/quick_start
    """

    def __init__(
        self,
        proxy_url: str = "http://litellm-proxy:4000",
        completion_model: Optional[str] = None,
        embedding_model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        api_key: str = "dummy",  # Proxy doesn't need real key if auth disabled
        timeout: float = 120.0,
    ):
        """Initialize LiteLLM proxy client.

        Args:
            proxy_url: LiteLLM proxy server URL
            completion_model: Model name from proxy config (e.g., "gpt-4o-mini")
            embedding_model: Embedding model name (e.g., "text-embedding-3-small")
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response
            api_key: API key for proxy (use "dummy" if auth disabled)
            timeout: Request timeout in seconds

        Note:
            Model names must match those in proxy's config.yaml model_list
        """
        self.proxy_url = proxy_url.rstrip("/")
        self.completion_model = completion_model
        self.embedding_model = embedding_model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_key = api_key
        self.timeout = timeout

        logger.info(
            f"LiteLLM proxy client initialized (proxy={proxy_url}, "
            f"completion={completion_model}, embedding={embedding_model})"
        )

    def _get_headers(self) -> dict:
        """Get HTTP headers for API requests."""
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def generate(
        self,
        prompt: Optional[str] = None,
        system_prompt: Optional[str] = None,
        prompt_variables: Optional[dict] = None,
        **kwargs
    ) -> str:
        """Generate text completion via proxy.

        Supports two modes:
        1. Dotprompt mode: Use .prompt files with template variables (preferred)
        2. Traditional mode: Direct prompt strings for standard chat completion

        Args:
            prompt: User prompt (used in traditional mode)
            system_prompt: System instructions (used in traditional mode)
            prompt_variables: Variables for .prompt file templating (dotprompt mode)
            **kwargs: Additional parameters (temperature, max_tokens, etc.)

        Returns:
            Generated text

        Raises:
            ValueError: If completion_model is not set or invalid arguments

        Examples:
            Dotprompt mode (uses .prompt file):
                >>> llm.generate(prompt_variables={"question": "What is RAG?", "context": "..."})

            Traditional mode:
                >>> llm.generate(prompt="Hello", system_prompt="You are helpful")
        """
        if not self.completion_model:
            raise ValueError("completion_model not set. Provide it in __init__")

        url = f"{self.proxy_url}/chat/completions"

        try:
            # Mode 1: Dotprompt with template variables
            if prompt_variables is not None:
                logger.debug(
                    f"Using dotprompt mode with variables: {list(prompt_variables.keys())}"
                )

                payload = {
                    "model": self.completion_model,
                    "messages": [{"role": "user", "content": "ignored"}],
                    "prompt_variables": prompt_variables,
                    "temperature": kwargs.get("temperature", self.temperature),
                    "max_tokens": kwargs.get("max_tokens", self.max_tokens),
                }

            # Mode 2: Traditional chat completion
            else:
                if prompt is None:
                    raise ValueError(
                        "Either 'prompt' or 'prompt_variables' must be provided"
                    )

                logger.debug("Using traditional chat completion mode")

                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})

                payload = {
                    "model": self.completion_model,
                    "messages": messages,
                    "temperature": kwargs.get("temperature", self.temperature),
                    "max_tokens": kwargs.get("max_tokens", self.max_tokens),
                }

            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    url,
                    headers=self._get_headers(),
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()

            content = data["choices"][0]["message"]["content"]

            logger.info(f"Generated (length={len(content)})")
            return content

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Generation failed: {e}", exc_info=True)
            raise

    def embed(self, texts: list[str], **kwargs) -> list[list[float]]:
        """Generate embeddings via proxy.

        Args:
            texts: List of texts to embed
            **kwargs: Additional parameters

        Returns:
            List of embedding vectors

        Raises:
            ValueError: If embedding_model is not set
        """
        if not self.embedding_model:
            raise ValueError("embedding_model not set. Provide it in __init__")

        url = f"{self.proxy_url}/embeddings"

        try:
            payload = {
                "model": self.embedding_model,
                "input": texts,
            }

            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(
                    url,
                    headers=self._get_headers(),
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()

            embeddings = [item["embedding"] for item in data["data"]]

            logger.info(f"Generated {len(embeddings)} embeddings")
            return embeddings

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Embedding failed: {e}", exc_info=True)
            raise
