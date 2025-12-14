"""Langfuse prompt manager for centralized prompt management."""

import os
from typing import Any, Optional

from langfuse import Langfuse

from libs.logger.logger import get_logger
from libs.llm.prompt_manager.base import BasePromptManager

logger = get_logger(__name__)


class LangfusePromptManager(BasePromptManager):
    """Langfuse client for centralized prompt management.

    Retrieves prompts from Langfuse prompt management system.

    Example:
        >>> pm = LangfusePromptManager(
        ...     public_key="pk-lf-...",
        ...     secret_key="sk-lf-...",
        ...     host="https://cloud.langfuse.com"
        ... )
        >>>
        >>> prompt = pm.get_prompt("triage_classifier")
        >>> compiled = prompt.compile(ticket_content="...", customer_id="...")
    """

    def __init__(
        self,
        public_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        host: Optional[str] = None,
        enabled: bool = True,
    ):
        """Initialize Langfuse prompt manager.

        Args:
            public_key: Langfuse public key (default: from LANGFUSE_PUBLIC_KEY env)
            secret_key: Langfuse secret key (default: from LANGFUSE_SECRET_KEY env)
            host: Langfuse host URL (default: from LANGFUSE_HOST env or cloud)
            enabled: Whether prompt manager is enabled
        """
        self.enabled = enabled
        self._available = False
        self.client: Optional[Langfuse] = None

        if not enabled:
            logger.info("Langfuse prompt manager disabled by configuration")
            return

        self.public_key = public_key or os.getenv("LANGFUSE_PUBLIC_KEY")
        self.secret_key = secret_key or os.getenv("LANGFUSE_SECRET_KEY")
        self.host = host or os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

        if not self.public_key or not self.secret_key:
            logger.warning(
                "Langfuse API keys not provided. Prompt manager will be disabled. "
                "Set LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY environment variables."
            )
            return

        try:
            self.client = Langfuse(
                public_key=self.public_key,
                secret_key=self.secret_key,
                host=self.host,
            )

            self._available = True
            logger.info(f"Langfuse prompt manager initialized (host={self.host})")

        except Exception as e:
            logger.error(f"Failed to initialize Langfuse prompt manager: {e}")

    def is_available(self) -> bool:
        """Check if Langfuse prompt manager is available."""
        return self._available and self.client is not None

    def get_prompt(
        self,
        name: str,
        version: Optional[int] = None,
        label: Optional[str] = None,
    ) -> Any:
        """Get a prompt from Langfuse.

        Args:
            name: Prompt name
            version: Specific version (optional)
            label: Label like "production" or "latest" (optional)

        Returns:
            Langfuse Prompt object with compile() method

        Raises:
            RuntimeError: If Langfuse is not available
            Exception: If prompt retrieval fails
        """
        if not self.is_available():
            raise RuntimeError(
                "Langfuse prompt manager is not available. Check API keys and connection."
            )

        try:
            if version is not None:
                prompt = self.client.get_prompt(name, version=version)
            elif label:
                prompt = self.client.get_prompt(name, label=label)
            else:
                prompt = self.client.get_prompt(name)

            logger.debug(f"Retrieved prompt '{name}' from Langfuse")
            return prompt

        except Exception as e:
            logger.error(f"Failed to get prompt '{name}' from Langfuse: {e}")
            raise

    def upload_prompt(
        self,
        name: str,
        prompt: str,
        config: Optional[dict] = None,
        labels: Optional[list] = None,
    ) -> Any:
        """Upload a prompt to Langfuse.

        Args:
            name: Prompt name
            prompt: Prompt template content
            config: Prompt configuration (model, temperature, etc.)
            labels: Labels to apply to the prompt

        Returns:
            Langfuse prompt creation result

        Raises:
            RuntimeError: If Langfuse is not available
            Exception: If prompt upload fails
        """
        if not self.is_available():
            raise RuntimeError(
                "Langfuse prompt manager is not available. Check API keys and connection."
            )

        try:
            result = self.client.create_prompt(
                name=name,
                prompt=prompt,
                config=config or {},
                labels=labels or [],
            )

            logger.info(f"Uploaded prompt '{name}' to Langfuse")
            return result

        except Exception as e:
            logger.error(f"Failed to upload prompt '{name}' to Langfuse: {e}")
            raise
