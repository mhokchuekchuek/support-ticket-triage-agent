"""Base abstraction for key-value databases."""

from abc import ABC, abstractmethod
from typing import Any


class BaseKeyValueClient(ABC):
    """Abstract base class for key-value databases.

    All key-value store implementations must inherit from this class
    and implement all abstract methods. This enables swapping between
    different key-value databases (Redis, Memcached, etc.) without
    changing application code.
    """

    @abstractmethod
    def get(self, **kwargs) -> Any:
        """Get value by key.

        Args:
            **kwargs: Implementation-specific parameters (e.g., key)

        Returns:
            Value if found, None otherwise.
        """
        pass

    @abstractmethod
    def set(self, **kwargs) -> bool:
        """Set key-value pair.

        Args:
            **kwargs: Implementation-specific parameters
                      (e.g., key, value, ttl)

        Returns:
            True if successful.
        """
        pass

    @abstractmethod
    def delete(self, **kwargs) -> bool:
        """Delete key(s).

        Args:
            **kwargs: Implementation-specific parameters (e.g., key, pattern)

        Returns:
            True if key was deleted.
        """
        pass

    @abstractmethod
    def scan(self, **kwargs) -> list[Any]:
        """Scan keys matching criteria.

        Args:
            **kwargs: Implementation-specific parameters (e.g., pattern)

        Returns:
            List of matching keys or values.
        """
        pass
