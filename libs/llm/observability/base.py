"""Base abstraction for observability tools."""

from abc import ABC, abstractmethod
from typing import Any


class BaseObservability(ABC):
    """Abstract base class for observability tool implementations.

    Provides minimal interface for LLM tracing.
    """

    @abstractmethod
    def trace_generation(self, **kwargs) -> Any:
        """Trace an LLM generation.

        Args:
            **kwargs: Provider-specific tracing parameters

        Returns:
            Provider-specific trace result
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if observability backend is available.

        Returns:
            True if backend is connected and operational
        """
        pass
