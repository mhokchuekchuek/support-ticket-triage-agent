# CheckpointRepository

Repository for LangGraph checkpoint operations.

## Location

`src/repositories/checkpoint/main.py`

## Overview

Abstracts LangGraph checkpoint and Redis key-value operations. Used for:
- Getting/saving checkpoint state
- Scanning active tickets
- Cleaning up Redis data

## Class

```python
class CheckpointRepository:
    def __init__(self, checkpointer: BaseCheckpointSaver, kv_client: BaseKeyValueClient)
    def get_checkpoint(self, customer_id: str, ticket_id: str) -> Optional[Any]
    def save_checkpoint(self, customer_id: str, ticket_id: str, checkpoint: dict, metadata: dict)
    def scan_active_ticket_ids(self, customer_id: str) -> list[str]
    def get_raw_checkpoint_data(self, customer_id: str, ticket_id: str) -> Optional[str]
    def delete_ticket_checkpoints(self, customer_id: str, ticket_id: str) -> int
```

## Dependencies

- `langgraph.checkpoint.base.BaseCheckpointSaver`
- `libs.database.keyvalue_db.base.BaseKeyValueClient`

## Usage

```python
from src.repositories.checkpoint.main import CheckpointRepository

checkpoint_repo = CheckpointRepository(checkpointer, kv_client)
active_tickets = checkpoint_repo.scan_active_ticket_ids("customer_123")
```

## See Also

- [TicketRepository](../ticket/README.md)
- [ChatRepository](../chat/README.md)
