"""Base abstraction for SQL databases."""

from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseSQLClient(ABC):
    """Abstract base class for SQL database clients.

    All SQL client implementations must inherit from this class and implement
    all abstract methods. This enables swapping between different SQL databases
    (PostgreSQL, MySQL, SQLite, etc.) without changing application code.
    """

    @abstractmethod
    def connect(self) -> None:
        """Establish database connection.

        Raises:
            Exception: If connection fails
        """
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Close database connection.

        Raises:
            Exception: If disconnection fails
        """
        pass

    @abstractmethod
    def execute(self, query: str, params: tuple = None) -> Any:
        """Execute a SQL query.

        Args:
            query: SQL query string with %s placeholders
            params: Query parameters

        Returns:
            Cursor or execution result

        Raises:
            Exception: If execution fails
        """
        pass

    @abstractmethod
    def fetch_one(self, query: str, params: tuple = None) -> Optional[dict]:
        """Fetch a single row as dictionary.

        Args:
            query: SQL query string with %s placeholders
            params: Query parameters

        Returns:
            Row as dictionary or None if no results

        Raises:
            Exception: If query fails
        """
        pass

    @abstractmethod
    def fetch_all(self, query: str, params: tuple = None) -> list[dict]:
        """Fetch all rows as list of dictionaries.

        Args:
            query: SQL query string with %s placeholders
            params: Query parameters

        Returns:
            List of rows as dictionaries

        Raises:
            Exception: If query fails
        """
        pass

    @abstractmethod
    def execute_many(self, query: str, params_list: list[tuple]) -> int:
        """Execute a query with multiple parameter sets.

        Args:
            query: SQL query string with %s placeholders
            params_list: List of parameter tuples

        Returns:
            Number of rows affected

        Raises:
            Exception: If execution fails
        """
        pass
