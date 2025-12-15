"""Repository for chat message persistence."""

from datetime import datetime

from libs.database.tabular.sql.base import BaseSQLClient


class ChatRepository:
    """Pure data access for chat message SQL operations.

    Handles chat message persistence in PostgreSQL.
    Contains NO business logic - only data access.

    Attributes:
        _db_client: SQL database client.
    """

    def __init__(self, db_client: BaseSQLClient):
        """Initialize chat repository.

        Args:
            db_client: SQL database client.
        """
        self._db_client = db_client

    def save_message(
        self,
        ticket_id: str,
        customer_id: str,
        role: str,
        content: str,
        created_at: datetime = None,
    ) -> None:
        """Save a single chat message.

        Args:
            ticket_id: Ticket identifier.
            customer_id: Customer identifier.
            role: Message role (human, ai).
            content: Message content.
            created_at: Message timestamp. Defaults to current UTC time.
        """
        if created_at is None:
            created_at = datetime.utcnow()

        self._db_client.execute(
            """
            INSERT INTO chat_messages (ticket_id, customer_id, role, content, created_at)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (ticket_id, customer_id, role, content, created_at),
        )

    def save_messages(
        self,
        ticket_id: str,
        customer_id: str,
        messages: list[dict],
    ) -> int:
        """Bulk save chat messages.

        Args:
            ticket_id: Ticket identifier.
            customer_id: Customer identifier.
            messages: List of message dicts with 'role' and 'content' keys.

        Returns:
            Number of messages saved.
        """
        created_at = datetime.utcnow()
        for msg in messages:
            self._db_client.execute(
                """
                INSERT INTO chat_messages (ticket_id, customer_id, role, content, created_at)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (ticket_id, customer_id, msg["role"], msg["content"], created_at),
            )
        return len(messages)

    def get_messages(self, ticket_id: str) -> list[dict]:
        """Get all messages for a ticket.

        Args:
            ticket_id: Ticket identifier.

        Returns:
            List of message records ordered by creation time.
        """
        return self._db_client.fetch_all(
            """
            SELECT ticket_id, customer_id, role, content, created_at
            FROM chat_messages
            WHERE ticket_id = %s
            ORDER BY created_at ASC
            """,
            (ticket_id,),
        )
