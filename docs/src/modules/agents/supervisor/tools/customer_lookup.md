# CustomerLookupTool

Look up customer information from PostgreSQL for classification decisions.

## Location

`src/modules/agents/supervisor/tools/customer_lookup.py`

## Classes

### `CustomerLookupInput`

Input schema for the tool.

| Field | Type | Description |
|-------|------|-------------|
| `customer_id` | str | Customer ID to look up |

### `CustomerLookupTool`

LangChain tool for querying customer data from PostgreSQL.

**Attributes**:

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | str | "customer_lookup" |
| `description` | str | Tool description for LLM |
| `db_client` | BaseSQLClient | PostgreSQL client |

## Constructor

```python
CustomerLookupTool(db_client: BaseSQLClient)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `db_client` | BaseSQLClient | SQL database client for queries |

## Methods

### `_run(customer_id) -> str`

Look up customer by ID from PostgreSQL.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `customer_id` | str | Customer ID to look up |

**Returns**: Formatted string with customer information.

**SQL Query**:
```sql
SELECT id, name, email, plan, tenure_months, region, seats, notes
FROM customers
WHERE id = %s
```

## Output Format

```
**Customer:** John Doe
**Email:** john@example.com
**Plan:** Enterprise
**Tenure:** 24 months
**Region:** North America
**Seats:** 50
**Notes:** VIP customer
```

## Usage

```python
from src.modules.agents.supervisor.tools.customer_lookup import CustomerLookupTool

# Initialize with PostgreSQL client
customer_tool = CustomerLookupTool(db_client=sql_client)

# Direct call
result = customer_tool._run(customer_id="cust_123")
```

## Error Handling

- Returns `"Customer {id} not found."` if no match
- Returns `"Error looking up customer: {error}"` on query failure

## See Also

- [SupervisorAgent](../README.md)
- [Database - Customers](/docs/db/customers.md)
