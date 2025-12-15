# PostgreSQL Client

PostgreSQL database client using psycopg2 with dictionary-based results.

## Location

`libs/database/tabular/sql/postgres/main.py`

## Class

### `PostgresSQLClient`

PostgreSQL database client with automatic connection management.

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `host` | str | `localhost` | Database server host |
| `port` | int | 5432 | Database server port |
| `database` | str | `support_triage` | Database name |
| `user` | str | `postgres` | Database user |
| `password` | str | `postgres` | Database password |
| `autocommit` | bool | True | Enable autocommit mode |

## Methods

### `connect() -> None`

Establish database connection.

### `disconnect() -> None`

Close database connection.

### `execute(query, params) -> Cursor`

Execute a SQL query.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | str | SQL query with %s placeholders |
| `params` | tuple | Query parameters |

**Returns**: Cursor after execution

### `fetch_one(query, params) -> Optional[dict]`

Fetch a single row as dictionary.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | str | SQL query with %s placeholders |
| `params` | tuple | Query parameters |

**Returns**: Row as dictionary or None

### `fetch_all(query, params) -> list[dict]`

Fetch all rows as list of dictionaries.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | str | SQL query with %s placeholders |
| `params` | tuple | Query parameters |

**Returns**: List of rows as dictionaries

### `execute_many(query, params_list) -> int`

Execute query with multiple parameter sets (batch insert).

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | str | SQL query with %s placeholders |
| `params_list` | list[tuple] | List of parameter tuples |

**Returns**: Number of rows affected

### `commit() -> None`

Commit current transaction.

### `rollback() -> None`

Rollback current transaction.

## Usage

```python
from libs.database.tabular.sql.selector import SQLClientSelector

# Using selector
client = SQLClientSelector.create(
    provider="postgres",
    host="postgres",
    port=5432,
    database="support_triage"
)

# Query single row
customer = client.fetch_one(
    "SELECT * FROM customers WHERE customer_id = %s",
    ("CUST001",)
)

# Query multiple rows
tickets = client.fetch_all(
    "SELECT * FROM tickets WHERE customer_id = %s AND status = %s",
    ("CUST001", "open")
)

# Insert with returning
client.execute(
    """
    INSERT INTO tickets (ticket_id, customer_id, status)
    VALUES (%s, %s, %s)
    """,
    ("TKT-001", "CUST001", "open")
)

# Batch insert
client.execute_many(
    "INSERT INTO chat_messages (ticket_id, role, content) VALUES (%s, %s, %s)",
    [
        ("TKT-001", "human", "Hello"),
        ("TKT-001", "ai", "Hi, how can I help?"),
    ]
)

# Using context manager
from libs.database.tabular.sql.postgres.main import PostgresSQLClient

with PostgresSQLClient(host="postgres", database="support_triage") as client:
    result = client.fetch_one("SELECT COUNT(*) as count FROM customers", None)
    print(f"Total customers: {result['count']}")
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_HOST` | Database host | `localhost` |
| `POSTGRES_PORT` | Database port | `5432` |
| `POSTGRES_DB` | Database name | `support_triage` |
| `POSTGRES_USER` | Database user | `postgres` |
| `POSTGRES_PASSWORD` | Database password | `postgres` |

## Dependencies

```
psycopg2-binary>=2.9.9
```
