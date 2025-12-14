"""Base abstraction for prompt manager tools."""

from abc import ABC, abstractmethod
from typing import Any, Optional


class BasePromptManager(ABC):
    """Abstract base class for prompt manager implementations.

    Provides minimal interface for prompt management.
    """

    @abstractmethod
    def get_prompt(
        self,
        name: str,
        version: Optional[int] = None,
        label: Optional[str] = None,
    ) -> Any:
        """Get a prompt by name.

        Args:
            name: Prompt name
            version: Specific version number (optional)
            label: Label like "production" or "latest" (optional)

        Returns:
            Prompt object
        """
        pass

    @abstractmethod
    def upload_prompt(
        self,
        name: str,
        prompt: str,
        config: Optional[dict] = None,
        labels: Optional[list] = None,
    ) -> Any:
        """Upload a prompt to the backend.

        Args:
            name: Prompt name
            prompt: Prompt template content
            config: Prompt configuration (model, temperature, etc.)
            labels: Labels to apply to the prompt

        Returns:
            Upload result
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if prompt manager backend is available.

        Returns:
            True if backend is connected and operational
        """
        pass
