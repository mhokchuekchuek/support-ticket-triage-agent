# Ticket Models

Support ticket input models for the triage system.

## Location

`src/entities/ticket.py`

## Classes

### `TicketMessage`

Single message in a support ticket conversation.

**Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `role` | str | Yes | Message sender: 'customer' or 'agent' |
| `content` | str | Yes | Message content |
| `timestamp` | datetime | No | Message timestamp (default: now) |

### `CustomerInfo`

Customer context for ticket triage.

**Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `plan` | str | Yes | Customer plan: free/pro/enterprise |
| `tenure_months` | int | Yes | How long customer has been active |
| `region` | str | No | Customer region if applicable |
| `seats` | int | No | Number of seats for enterprise |
| `previous_tickets` | int | No | Number of previous support tickets (default: 0) |

### `Ticket`

Support ticket input model.

**Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ticket_id` | str | Yes | Unique ticket identifier |
| `customer_id` | str | Yes | Customer identifier |
| `customer_info` | CustomerInfo | Yes | Customer context |
| `messages` | list[TicketMessage] | Yes | Conversation messages in chronological order |
| `metadata` | dict[str, Any] | No | Additional metadata |

## Usage

```python
from src.entities.ticket import Ticket, TicketMessage, CustomerInfo
from datetime import datetime, timedelta

# Create customer info
customer = CustomerInfo(
    plan="enterprise",
    tenure_months=8,
    region="Thailand",
    seats=45,
    previous_tickets=0
)

# Create messages
messages = [
    TicketMessage(
        role="customer",
        content="System showing error 500",
        timestamp=datetime.now() - timedelta(hours=2)
    ),
    TicketMessage(
        role="customer",
        content="Multiple users affected",
        timestamp=datetime.now() - timedelta(hours=1)
    )
]

# Create ticket
ticket = Ticket(
    ticket_id="T-12345",
    customer_id="C-001",
    customer_info=customer,
    messages=messages
)
```
