"""Chat message entity for SQL storage."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Chat message for SQL storage.

    Represents a single message in a support ticket conversation,
    stored in the PostgreSQL database for permanent history.

    Attributes:
        id: Database primary key (auto-generated).
        ticket_id: Associated ticket identifier.
        role: Message sender role (human/ai).
        content: Message content text.
        metadata: Optional metadata as JSON.
        created_at: When the message was sent.
    """

    id: Optional[int] = Field(default=None, description="Database primary key")
    ticket_id: str = Field(..., description="Associated ticket identifier")
    role: str = Field(..., description="Message sender: 'human' or 'ai'")
    content: str = Field(..., description="Message content")
    metadata: Optional[dict] = Field(default=None, description="Optional metadata")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Message timestamp"
    )
