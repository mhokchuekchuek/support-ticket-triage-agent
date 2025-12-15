# ChatRepository

Repository for chat message persistence.

## Location

`src/repositories/chat/main.py`

## Overview

Handles chat message persistence in PostgreSQL. Used for:
- Saving single messages
- Bulk saving messages
- Getting messages for a ticket

## Class

```python
class ChatRepository:
    def __init__(self, db_client: BaseSQLClient)
    def save_message(self, ticket_id: str, customer_id: str, role: str, content: str, created_at: datetime)
    def save_messages(self, ticket_id: str, customer_id: str, messages: list[dict]) -> int
    def get_messages(self, ticket_id: str) -> list[dict]
```

## Dependencies

- `libs.database.tabular.sql.base.BaseSQLClient`

## Usage

```python
from src.repositories.chat.main import ChatRepository

chat_repo = ChatRepository(sql_client)
messages = [{"role": "human", "content": "Hello"}, {"role": "ai", "content": "Hi!"}]
count = chat_repo.save_messages("ticket_123", "customer_123", messages)
```

## See Also

- [CheckpointRepository](../checkpoint/README.md)
- [TicketRepository](../ticket/README.md)
