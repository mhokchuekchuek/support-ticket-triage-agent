from pydantic import BaseModel, Field
from typing import Optional, Any
from datetime import datetime


class TicketMessage(BaseModel):
    """Single message in a support ticket conversation.

    Attributes:
        role: Message sender - 'customer' or 'agent'.
        content: The message text content.
        timestamp: When the message was sent.
    """

    role: str = Field(..., description="Message sender: 'customer' or 'agent'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Message timestamp"
    )


class CustomerInfo(BaseModel):
    """Customer context for ticket triage.

    Contains relevant customer information that helps determine
    ticket priority and routing decisions.

    Attributes:
        plan: Customer subscription plan (free/pro/enterprise).
        tenure_months: How long customer has been active.
        region: Customer region if applicable.
        seats: Number of seats for enterprise plans.
        previous_tickets: Number of previous support tickets.
    """

    plan: str = Field(..., description="Customer plan: free/pro/enterprise")
    tenure_months: int = Field(..., description="How long customer has been active")
    region: Optional[str] = Field(None, description="Customer region if applicable")
    seats: Optional[int] = Field(None, description="Number of seats for enterprise")
    previous_tickets: int = Field(
        default=0, description="Number of previous support tickets"
    )


class Ticket(BaseModel):
    """Support ticket input model.

    Represents an incoming customer support ticket with full
    conversation history and customer context.

    Attributes:
        ticket_id: Unique ticket identifier.
        customer_id: Customer identifier.
        customer_info: Customer context for triage decisions.
        messages: Conversation messages in chronological order.
        metadata: Additional metadata if needed.
    """

    ticket_id: str = Field(..., description="Unique ticket identifier")
    customer_id: str = Field(..., description="Customer identifier")
    customer_info: CustomerInfo = Field(..., description="Customer context")
    messages: list[TicketMessage] = Field(
        ..., description="Conversation messages in chronological order"
    )
    metadata: Optional[dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )
