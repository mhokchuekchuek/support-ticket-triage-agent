"""PostgreSQL database client.

Implements SQL operations using psycopg2.

Reference: https://www.psycopg.org/docs/
"""

from typing import Any, Optional

import psycopg2
from psycopg2.extras import RealDictCursor

from libs.database.tabular.sql.base import BaseSQLClient
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class PostgresSQLClient(BaseSQLClient):
    """PostgreSQL database client using psycopg2.

    Provides SQL operations with automatic connection management and
    dictionary-based results using RealDictCursor.

    Features:
    - Connection pooling (optional)
    - Dictionary results via RealDictCursor
    - Transaction support
    - Parameterized queries for SQL injection prevention

    Reference: https://www.psycopg.org/docs/
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        database: str = "support_triage",
        user: str = "postgres",
        password: str = "postgres",
        autocommit: bool = True,
    ):
        """Initialize PostgreSQL client.

        Args:
            host: Database server host (default: "localhost")
            port: Database server port (default: 5432)
            database: Database name (default: "support_triage")
            user: Database user (default: "postgres")
            password: Database password (default: "postgres")
            autocommit: Enable autocommit mode (default: True)

        Note:
            For Docker Compose, use host="postgres" to connect to the service
        """
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.autocommit = autocommit
        self._conn = None

        logger.info(
            f"PostgreSQL client initialized (host={host}:{port}, "
            f"database={database})"
        )

    @property
    def conn(self):
        """Get database connection, creating if needed."""
        if self._conn is None or self._conn.closed:
            self.connect()
        return self._conn

    def connect(self) -> None:
        """Establish database connection.

        Raises:
            Exception: If connection fails
        """
        try:
            self._conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
            )
            self._conn.autocommit = self.autocommit
            logger.info(f"Connected to PostgreSQL database '{self.database}'")

        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL: {e}", exc_info=True)
            raise

    def disconnect(self) -> None:
        """Close database connection.

        Raises:
            Exception: If disconnection fails
        """
        try:
            if self._conn and not self._conn.closed:
                self._conn.close()
                logger.info("Disconnected from PostgreSQL")

        except Exception as e:
            logger.error(f"Failed to disconnect from PostgreSQL: {e}", exc_info=True)
            raise

    def execute(self, query: str, params: tuple = None) -> Any:
        """Execute a SQL query.

        Args:
            query: SQL query string with %s placeholders
            params: Query parameters

        Returns:
            Cursor after execution

        Raises:
            Exception: If execution fails
        """
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            return cursor

        except Exception as e:
            logger.error(f"Query execution failed: {e}", exc_info=True)
            raise

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
        try:
            cursor = self.execute(query, params)
            result = cursor.fetchone()
            cursor.close()

            if result:
                return dict(result)
            return None

        except Exception as e:
            logger.error(f"Fetch one failed: {e}", exc_info=True)
            raise

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
        try:
            cursor = self.execute(query, params)
            results = cursor.fetchall()
            cursor.close()

            return [dict(row) for row in results]

        except Exception as e:
            logger.error(f"Fetch all failed: {e}", exc_info=True)
            raise

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
        try:
            cursor = self.conn.cursor()
            cursor.executemany(query, params_list)
            rowcount = cursor.rowcount
            cursor.close()

            logger.info(f"Executed batch query, {rowcount} rows affected")
            return rowcount

        except Exception as e:
            logger.error(f"Batch execution failed: {e}", exc_info=True)
            raise

    def commit(self) -> None:
        """Commit current transaction."""
        if self._conn and not self._conn.closed:
            self._conn.commit()

    def rollback(self) -> None:
        """Rollback current transaction."""
        if self._conn and not self._conn.closed:
            self._conn.rollback()

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
