"""Tool for summarizing ticket from Redis checkpoint data."""

import json
from typing import Type, Optional

from langchain.tools import BaseTool
from pydantic import Field, BaseModel

from libs.database.keyvalue_db.base import BaseKeyValueClient
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class TicketSummarizeInput(BaseModel):
    """Input schema for ticket summarize tool."""

    ticket_id: str = Field(description="Ticket ID to summarize")
    customer_id: str = Field(description="Customer ID")


class TicketSummarizeTool(BaseTool):
    """Summarize ticket from Redis checkpoint data.

    Reads LangGraph checkpoint from Redis and extracts key information
    to create a summary for ticket matching.

    Attributes:
        name: Tool name for LangChain.
        description: Tool description for the LLM.
        kv_client: Key-value client for Redis.
    """

    name: str = "ticket_summarize"
    description: str = (
        "Summarize an active ticket from Redis checkpoint. "
        "Returns ticket type, recent messages, and current status."
    )
    args_schema: Type[BaseModel] = TicketSummarizeInput
    kv_client: Optional[BaseKeyValueClient] = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, kv_client: BaseKeyValueClient, **kwargs):
        """Initialize ticket summarize tool.

        Args:
            kv_client: Key-value client for Redis.
            **kwargs: Additional arguments passed to BaseTool.
        """
        super().__init__(**kwargs)
        self.kv_client = kv_client
        logger.info("TicketSummarizeTool initialized")

    def _run(self, ticket_id: str, customer_id: str) -> str:
        """Summarize ticket from Redis checkpoint.

        Args:
            ticket_id: Ticket ID to summarize.
            customer_id: Customer ID.

        Returns:
            Formatted summary string.
        """
        logger.info(f"Summarizing ticket: {ticket_id}")

        try:
            # Scan for checkpoint keys
            thread_id = f"{customer_id}:{ticket_id}"
            pattern = f"*{thread_id}*"
            keys = self.kv_client.scan(pattern=pattern)

            if not keys:
                return f"No checkpoint found for ticket {ticket_id}"

            # Find the checkpoint data key (usually contains 'checkpoint' or 'writes')
            checkpoint_data = None
            for key in keys:
                value = self.kv_client.get(key=key)
                if value:
                    try:
                        data = json.loads(value) if isinstance(value, str) else value
                        if isinstance(data, dict):
                            checkpoint_data = data
                            break
                    except (json.JSONDecodeError, TypeError):
                        continue

            if not checkpoint_data:
                return f"Could not parse checkpoint for ticket {ticket_id}"

            # Extract summary from checkpoint
            summary = self._extract_summary(ticket_id, checkpoint_data)
            return summary

        except Exception as e:
            logger.error(f"Failed to summarize ticket {ticket_id}: {e}")
            return f"Error summarizing ticket {ticket_id}: {str(e)}"

    def _extract_summary(self, ticket_id: str, checkpoint: dict) -> str:
        """Extract summary from checkpoint data.

        Args:
            ticket_id: Ticket ID.
            checkpoint: Parsed checkpoint data.

        Returns:
            Summary string.
        """
        # Try to extract from channel_values (LangGraph state)
        channel_values = checkpoint.get("channel_values", checkpoint)

        # Extract ticket info
        ticket = channel_values.get("ticket", {})
        ticket_type = "unknown"
        urgency = "unknown"
        last_message = "No messages"

        # Get supervisor decision if available
        supervisor_decision = channel_values.get("supervisor_decision")
        if supervisor_decision:
            if hasattr(supervisor_decision, "ticket_type"):
                ticket_type = supervisor_decision.ticket_type.value
            elif isinstance(supervisor_decision, dict):
                ticket_type = supervisor_decision.get("ticket_type", "unknown")

            if hasattr(supervisor_decision, "urgency"):
                urgency = supervisor_decision.urgency.value
            elif isinstance(supervisor_decision, dict):
                urgency = supervisor_decision.get("urgency", "unknown")

        # Get last message from ticket
        if isinstance(ticket, dict):
            messages = ticket.get("messages", [])
            if messages:
                last_msg = messages[-1]
                if isinstance(last_msg, dict):
                    last_message = last_msg.get("content", "")[:100]
                elif hasattr(last_msg, "content"):
                    last_message = last_msg.content[:100]

        # Get current agent
        current_agent = channel_values.get("current_agent", "unknown")

        return (
            f"**Ticket {ticket_id}**\n"
            f"Type: {ticket_type}\n"
            f"Urgency: {urgency}\n"
            f"Current Stage: {current_agent}\n"
            f"Last Message: {last_message}..."
        )
