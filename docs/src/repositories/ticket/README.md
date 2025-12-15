# TicketRepository

Repository for ticket persistence operations.

## Location

`src/repositories/ticket/main.py`

## Overview

Handles ticket CRUD operations in PostgreSQL. Used for:
- Saving ticket records
- Getting ticket by ID
- Getting customer ticket history
- Getting open tickets

## Class

```python
class TicketRepository:
    def __init__(self, db_client: BaseSQLClient)
    def save_ticket(self, ticket_id: str, customer_id: str, status: str, urgency: str, ticket_type: str, triage_result: dict, closed_at: Optional[datetime])
    def get_ticket(self, ticket_id: str) -> Optional[dict]
    def get_customer_history(self, customer_id: str, limit: int) -> list[dict]
    def get_open_tickets(self, customer_id: str) -> list[dict]
```

## Dependencies

- `libs.database.tabular.sql.base.BaseSQLClient`

## Usage

```python
from src.repositories.ticket.main import TicketRepository

ticket_repo = TicketRepository(sql_client)
history = ticket_repo.get_customer_history("customer_123", limit=10)
```

## See Also

- [CheckpointRepository](../checkpoint/README.md)
- [ChatRepository](../chat/README.md)
