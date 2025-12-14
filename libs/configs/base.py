"""Base abstraction for configuration management."""

from abc import ABC, abstractmethod
from typing import Any


class BaseConfigManager(ABC):
    """Abstract base class for configuration managers.

    All configuration manager implementations must inherit from this class
    and implement all abstract methods.
    """

    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key.

        Args:
            key: Configuration key (supports nested keys with dot notation)
            default: Default value if key is not found

        Returns:
            Configuration value or default
        """
        pass

    @abstractmethod
    def as_dict(self) -> dict[str, Any]:
        """Get all configuration as a dictionary.

        Returns:
            Dictionary containing all configuration values
        """
        pass

    @abstractmethod
    def __getattr__(self, name: str) -> Any:
        """Get configuration value as attribute.

        Args:
            name: Configuration key

        Returns:
            Configuration value

        Raises:
            AttributeError: If key is not found
        """
        pass
