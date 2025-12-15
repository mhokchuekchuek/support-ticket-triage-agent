"""Repository for ticket persistence operations."""

import json
from datetime import datetime
from typing import Optional

from libs.database.tabular.sql.base import BaseSQLClient


class TicketRepository:
    """Pure data access for ticket SQL operations.

    Handles ticket CRUD operations in PostgreSQL.
    Contains NO business logic - only data access.

    Attributes:
        _db_client: SQL database client.
    """

    def __init__(self, db_client: BaseSQLClient):
        """Initialize ticket repository.

        Args:
            db_client: SQL database client.
        """
        self._db_client = db_client

    def save_ticket(
        self,
        ticket_id: str,
        customer_id: str,
        status: str,
        urgency: str,
        ticket_type: str,
        triage_result: dict,
        closed_at: Optional[datetime] = None,
    ) -> None:
        """Insert or update ticket record.

        Args:
            ticket_id: Unique ticket identifier.
            customer_id: Customer identifier.
            status: Ticket status (open, closed).
            urgency: Urgency level.
            ticket_type: Type of ticket (billing, technical, general).
            triage_result: Triage result data.
            closed_at: Timestamp when ticket was closed.
        """
        self._db_client.execute(
            """
            INSERT INTO tickets (
                ticket_id, customer_id, status, urgency, ticket_type, triage_result, closed_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (ticket_id) DO UPDATE SET
                status = EXCLUDED.status,
                urgency = EXCLUDED.urgency,
                ticket_type = EXCLUDED.ticket_type,
                triage_result = EXCLUDED.triage_result,
                closed_at = EXCLUDED.closed_at
            """,
            (
                ticket_id,
                customer_id,
                status,
                urgency,
                ticket_type,
                json.dumps(triage_result),
                closed_at,
            ),
        )

    def get_ticket(self, ticket_id: str) -> Optional[dict]:
        """Get ticket by ID.

        Args:
            ticket_id: Ticket identifier.

        Returns:
            Ticket record as dict if found, None otherwise.
        """
        return self._db_client.fetch_one(
            """
            SELECT ticket_id, customer_id, status, urgency, ticket_type,
                   triage_result, created_at, closed_at
            FROM tickets
            WHERE ticket_id = %s
            """,
            (ticket_id,),
        )

    def get_customer_history(self, customer_id: str, limit: int = 10) -> list[dict]:
        """Get closed ticket history for customer.

        Args:
            customer_id: Customer identifier.
            limit: Maximum number of tickets to return.

        Returns:
            List of ticket records.
        """
        return self._db_client.fetch_all(
            """
            SELECT ticket_id, ticket_type, urgency, status, triage_result,
                   created_at, closed_at
            FROM tickets
            WHERE customer_id = %s
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (customer_id, limit),
        )

    def get_open_tickets(self, customer_id: str) -> list[dict]:
        """Get open tickets for customer.

        Args:
            customer_id: Customer identifier.

        Returns:
            List of open ticket records.
        """
        return self._db_client.fetch_all(
            """
            SELECT ticket_id, ticket_type, urgency, status, created_at
            FROM tickets
            WHERE customer_id = %s AND status = 'open'
            ORDER BY created_at DESC
            """,
            (customer_id,),
        )
