from abc import ABC, abstractmethod
from typing import Any

from libs.logger.logger import get_logger


class BaseAgent(ABC):
    """Abstract base class for all agents.

    All agents should inherit from this class and implement
    the execute method to process the agent state.

    Attributes:
        name: Unique identifier for this agent.
        logger: Logger instance for this agent.
    """

    def __init__(self, name: str):
        """Initialize the agent.

        Args:
            name: Unique identifier for this agent.
        """
        self.name = name
        self.logger = get_logger(f"agent.{name}")

    @abstractmethod
    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        """Execute the agent's logic on the current state.

        Args:
            state: Current agent state with messages, ticket, etc.

        Returns:
            Updated agent state after processing.
        """
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
