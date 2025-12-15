"""Repository for LangGraph checkpoint operations."""

from typing import Optional, Any

from langgraph.checkpoint.base import BaseCheckpointSaver

from libs.database.keyvalue_db.base import BaseKeyValueClient


class CheckpointRepository:
    """Pure data access for checkpoint/Redis operations.

    Abstracts LangGraph checkpoint and Redis key-value operations.
    Contains NO business logic - only data access.

    Attributes:
        _checkpointer: LangGraph checkpoint saver.
        _kv_client: Key-value client for Redis operations.
    """

    def __init__(
        self,
        checkpointer: BaseCheckpointSaver,
        kv_client: BaseKeyValueClient,
    ):
        """Initialize checkpoint repository.

        Args:
            checkpointer: LangGraph checkpoint saver.
            kv_client: Key-value client for Redis.
        """
        self._checkpointer = checkpointer
        self._kv_client = kv_client

    def get_checkpoint(self, customer_id: str, ticket_id: str) -> Optional[Any]:
        """Get checkpoint tuple for a ticket.

        Args:
            customer_id: Customer identifier.
            ticket_id: Ticket identifier.

        Returns:
            Checkpoint tuple if found, None otherwise.
        """
        config = {"configurable": {"thread_id": f"{customer_id}:{ticket_id}"}}
        return self._checkpointer.get_tuple(config)

    def save_checkpoint(
        self,
        customer_id: str,
        ticket_id: str,
        checkpoint: dict,
        metadata: dict,
    ) -> None:
        """Save checkpoint data.

        Args:
            customer_id: Customer identifier.
            ticket_id: Ticket identifier.
            checkpoint: Checkpoint data to save.
            metadata: Checkpoint metadata.
        """
        config = {"configurable": {"thread_id": f"{customer_id}:{ticket_id}"}}
        self._checkpointer.put(config, checkpoint, metadata, {})

    def scan_activated_ticket_ids(self, customer_id: str) -> list[str]:
        """Scan Redis for customer's activated ticket IDs.

        Args:
            customer_id: Customer identifier.

        Returns:
            List of activated ticket IDs.
        """
        pattern = f"*{customer_id}:*"
        keys = self._kv_client.scan(pattern=pattern)

        ticket_ids = set()
        for key in keys:
            parts = key.split(":")
            for i, part in enumerate(parts):
                if part == customer_id and i + 1 < len(parts):
                    ticket_ids.add(parts[i + 1])
                    break
        return list(ticket_ids)

    def get_raw_checkpoint_data(
        self,
        customer_id: str,
        ticket_id: str,
    ) -> Optional[str]:
        """Get raw checkpoint data for summarization.

        Args:
            customer_id: Customer identifier.
            ticket_id: Ticket identifier.

        Returns:
            Raw checkpoint data string if found, None otherwise.
        """
        thread_id = f"{customer_id}:{ticket_id}"
        pattern = f"*{thread_id}*"
        keys = self._kv_client.scan(pattern=pattern)
        if keys:
            return self._kv_client.get(key=keys[0])
        return None

    def delete_ticket_checkpoints(self, customer_id: str, ticket_id: str) -> int:
        """Delete all checkpoint data for a ticket.

        Args:
            customer_id: Customer identifier.
            ticket_id: Ticket identifier.

        Returns:
            Number of keys deleted.
        """
        pattern = f"*{customer_id}*{ticket_id}*"
        keys = self._kv_client.scan(pattern=pattern)
        if keys:
            self._kv_client.delete(pattern=pattern)
        return len(keys)
