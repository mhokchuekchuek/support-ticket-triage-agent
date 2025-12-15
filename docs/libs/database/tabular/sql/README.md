# SQL Database

SQL database implementations using the provider/selector pattern.

## Location

`libs/database/tabular/sql/`

## Providers

| Provider | Description | Documentation |
|----------|-------------|---------------|
| `postgres` | PostgreSQL database | [postgres.md](postgres.md) |

## Classes

### BaseSQLClient

Abstract base class for SQL databases.

**Location**: `libs/database/tabular/sql/base.py`

**Methods**:

| Method | Description |
|--------|-------------|
| `connect()` | Establish database connection |
| `disconnect()` | Close database connection |
| `execute(query, params)` | Execute a SQL query |
| `fetch_one(query, params)` | Fetch a single row as dictionary |
| `fetch_all(query, params)` | Fetch all rows as list of dictionaries |
| `execute_many(query, params_list)` | Execute query with multiple parameter sets |

### SQLClientSelector

Selector for SQL database providers.

**Location**: `libs/database/tabular/sql/selector.py`

**Methods**:

| Method | Description |
|--------|-------------|
| `create(provider, **kwargs)` | Create SQL client instance |
| `list_providers()` | List available providers |

## Usage

```python
from libs.database.tabular.sql.selector import SQLClientSelector

# Create PostgreSQL client
client = SQLClientSelector.create(
    provider="postgres",
    host="localhost",
    port=5432,
    database="support_triage",
    user="postgres",
    password="postgres"
)

# Query data
customer = client.fetch_one(
    "SELECT * FROM customers WHERE customer_id = %s",
    ("CUST001",)
)

# Insert data
client.execute(
    "INSERT INTO customers (customer_id, name) VALUES (%s, %s)",
    ("CUST002", "John Doe")
)

# Fetch multiple rows
messages = client.fetch_all(
    "SELECT * FROM chat_messages WHERE ticket_id = %s",
    ("TKT-001",)
)
```
