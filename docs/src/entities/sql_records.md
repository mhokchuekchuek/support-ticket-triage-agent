# SQL Record Entities

Database record models for PostgreSQL storage.

## Location

- `src/entities/customer_record.py`
- `src/entities/chat_message.py`

## Models

### CustomerRecord

Customer record for SQL storage.

**Location**: `src/entities/customer_record.py`

**Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | str | Yes | Unique customer identifier (primary key) |
| `name` | str | Yes | Customer name |
| `email` | str | Yes | Customer email |
| `plan` | str | Yes | Customer plan: free/pro/enterprise |
| `tenure_months` | int | Yes | Months as customer |
| `region` | str | No | Customer region |
| `seats` | int | No | Number of seats (default: 1) |
| `notes` | str | No | Additional notes |
| `created_at` | datetime | No | Record creation timestamp |

### ChatMessage

Chat message for SQL storage.

**Location**: `src/entities/chat_message.py`

**Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ticket_id` | str | Yes | Associated ticket identifier |
| `customer_id` | str | Yes | Associated customer identifier |
| `role` | str | Yes | Message sender: 'human' or 'ai' |
| `content` | str | Yes | Message content |
| `created_at` | datetime | Yes | Message timestamp (part of primary key) |

**Primary Key**: `(ticket_id, created_at)`

## Usage

```python
from src.entities.customer_record import CustomerRecord
from src.entities.chat_message import ChatMessage

# Create customer record
customer = CustomerRecord(
    id="CUST001",
    name="John Doe",
    email="john@example.com",
    plan="enterprise",
    tenure_months=24,
    region="US",
    seats=50
)

# Create chat message
message = ChatMessage(
    ticket_id="TKT-001",
    customer_id="CUST001",
    role="human",
    content="I need help with my invoice"
)
```

## Database Tables

These entities map to PostgreSQL tables:

| Entity | Table | Documentation |
|--------|-------|---------------|
| `CustomerRecord` | `customers` | [/docs/db/customers.md](/docs/db/customers.md) |
| `ChatMessage` | `chat_messages` | [/docs/db/chat_messages.md](/docs/db/chat_messages.md) |

See [Database Documentation](/docs/db/README.md) for table schemas.

## See Also

- [TicketPersistenceAgent](../modules/agents/ticket_persistence/README.md) - Saves chat messages on ticket completion
- [Database Documentation](/docs/db/README.md) - Complete database architecture
