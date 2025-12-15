"""Customer record entity for SQL storage."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CustomerRecord(BaseModel):
    """Customer record for SQL storage.

    Represents a customer stored in the PostgreSQL database.
    This is separate from CustomerInfo which is used for ticket input.

    Attributes:
        id: Database primary key (auto-generated).
        customer_id: Unique customer identifier.
        name: Customer name.
        email: Customer email address.
        plan: Customer plan (free/pro/enterprise).
        tenure_months: How long customer has been active.
        region: Customer region if applicable.
        seats: Number of seats for enterprise plans.
        notes: Additional notes about the customer.
        previous_tickets: List of previous ticket records.
        created_at: When the record was created.
    """

    id: Optional[int] = Field(default=None, description="Database primary key")
    customer_id: str = Field(..., description="Unique customer identifier")
    name: Optional[str] = Field(default=None, description="Customer name")
    email: Optional[str] = Field(default=None, description="Customer email")
    plan: str = Field(..., description="Customer plan: free/pro/enterprise")
    tenure_months: int = Field(..., description="Months as customer")
    region: Optional[str] = Field(default=None, description="Customer region")
    seats: int = Field(default=1, description="Number of seats")
    notes: Optional[str] = Field(default=None, description="Additional notes")
    previous_tickets: list[dict] = Field(
        default_factory=list, description="Previous ticket records"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Record creation timestamp"
    )
