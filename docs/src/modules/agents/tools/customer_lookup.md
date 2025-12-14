# CustomerLookupTool

Look up customer information by customer ID.

## Location

`src/modules/agents/tools/customer_lookup.py`

## Classes

### `CustomerLookupInput`

Input schema for the tool.

| Field | Type | Description |
|-------|------|-------------|
| `customer_id` | str | Customer ID to look up |

### `CustomerLookupTool`

LangChain tool for looking up customer information.

**Attributes**:

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | str | "customer_lookup" |
| `description` | str | Tool description for LLM |
| `customers_data` | dict | Loaded customer data |

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data_path` | str | "data/customers.json" | Path to customers JSON file |

## Methods

### `_run(customer_id) -> str`

Look up customer by ID.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `customer_id` | str | Customer ID to look up |

**Returns**: Formatted string with customer information.

## Data Format

The customers JSON file should have this structure:

```json
{
  "customers": [
    {
      "id": "C-001",
      "name": "John Doe",
      "email": "john@example.com",
      "plan": "pro",
      "tenure_months": 5,
      "region": "US",
      "seats": 1,
      "previous_tickets": [],
      "notes": "Active user"
    }
  ]
}
```

## Usage

```python
from src.modules.agents.tools.customer_lookup import CustomerLookupTool

tool = CustomerLookupTool(data_path="data/customers.json")

# Direct call
result = tool._run(customer_id="C-001")
```
