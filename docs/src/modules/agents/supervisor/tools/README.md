# Supervisor Agent Tools

LangChain tools for the SupervisorAgent.

## Location

`src/modules/agents/supervisor/tools/`

## Tools

| Tool | File | Description |
|------|------|-------------|
| `CustomerLookupTool` | `customer_lookup.py` | Query customer info from PostgreSQL |

## CustomerLookupTool

Queries the PostgreSQL `customers` table to retrieve customer context for classification decisions.

```python
from src.modules.agents.supervisor.tools.customer_lookup import CustomerLookupTool

customer_tool = CustomerLookupTool(db_client=sql_client)
```

Returns: name, email, plan, tenure, region, seats, notes

## See Also

- [SupervisorAgent](../README.md)
- [CustomerLookupTool Details](customer_lookup.md)
