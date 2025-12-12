"""Base tool selector for dynamic provider selection."""

import importlib
from typing import Any

from libs.logger.logger import get_logger

logger = get_logger(__name__)


class BaseToolSelector:
    """Base class for tool selectors with provider-based selection.

    Subclasses define _PROVIDERS dict mapping provider names to module paths.

    Example:
        >>> class LLMClientSelector(BaseToolSelector):
        ...     _PROVIDERS = {
        ...         "litellm": "libs.llm.client.litellm.main.LLMClient",
        ...     }
        >>> client = LLMClientSelector.create("litellm", proxy_url="...")
    """

    _PROVIDERS: dict[str, str] = {}  # Override in subclass

    @classmethod
    def create(cls, provider: str, **kwargs) -> Any:
        """Select and instantiate tool based on provider.

        Args:
            provider: Provider name (must be in _PROVIDERS)
            **kwargs: Provider-specific initialization parameters

        Returns:
            Tool instance

        Raises:
            ValueError: If provider is unknown or class cannot be loaded
        """
        if not cls._PROVIDERS:
            raise ValueError(
                f"{cls.__name__} has no providers defined. "
                f"Override _PROVIDERS in subclass."
            )

        if provider not in cls._PROVIDERS:
            available = ", ".join(cls._PROVIDERS.keys())
            raise ValueError(
                f"Unknown provider '{provider}' for {cls.__name__}. "
                f"Available providers: {available}"
            )

        try:
            full_path = cls._PROVIDERS[provider]
            module_path, class_name = full_path.rsplit(".", 1)
            module = importlib.import_module(module_path)

            if not hasattr(module, class_name):
                raise AttributeError(
                    f"Class '{class_name}' not found in module '{module_path}'"
                )

            ToolClass = getattr(module, class_name)

            logger.info(
                f"{cls.__name__}: Creating {class_name} with provider '{provider}'"
            )
            return ToolClass(**kwargs)

        except ImportError as e:
            raise ValueError(
                f"Cannot import module for provider '{provider}': {e}"
            ) from e
        except Exception as e:
            raise ValueError(
                f"Failed to create tool for provider '{provider}': {e}"
            ) from e

    @classmethod
    def list_providers(cls) -> list[str]:
        """List available providers for this tool."""
        return list(cls._PROVIDERS.keys())
