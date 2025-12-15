# SupervisorAgent

Supervisor agent for ticket classification and routing.

## Location

`src/modules/agents/supervisor/`

## Structure

```
supervisor/
├── __init__.py
├── main.py                         # SupervisorAgent
└── tools/
    ├── __init__.py
    └── customer_lookup.py          # CustomerLookupTool
```

## Overview

Classifies urgency level and ticket type, then routes to the appropriate specialist agent:
- Uses `customer_lookup` tool to get customer context from PostgreSQL
- Classifies urgency: critical / high / medium / low
- Determines ticket type: billing / technical / general
- Decides if direct escalation is needed

## Class

```python
class SupervisorAgent(BaseAgent):
    def __init__(
        self,
        llm,
        tools: List[BaseTool],
        observability: Optional[any] = None,
        prompt_manager: Optional[any] = None,
        agent_config: Optional[dict] = None,
    ):
        ...
```

## Tools

### CustomerLookupTool

Looks up customer information from PostgreSQL `customers` table, including plan type, tenure, region, seats, and account notes.

**Location**: `src/modules/agents/supervisor/tools/customer_lookup.py`

```python
from src.modules.agents.supervisor.tools.customer_lookup import CustomerLookupTool

tool = CustomerLookupTool(db_client=sql_client)
```

## Usage

```python
from src.modules.agents.supervisor.main import SupervisorAgent
from src.modules.agents.supervisor.tools.customer_lookup import CustomerLookupTool

customer_tool = CustomerLookupTool(db_client=sql_client)

agent = SupervisorAgent(
    llm=llm,
    tools=[customer_tool],
    prompt_manager=prompt_manager,
    agent_config=config,
)
```

## Output

Returns `SupervisorDecision`:
- `urgency`: UrgencyLevel (critical/high/medium/low)
- `ticket_type`: TicketType (billing/technical/general)
- `reasoning`: Classification reasoning
- `requires_escalation`: Whether to skip specialist

## See Also

- [BaseAgent](../base.md)
- [Agent Flow](../../graph/agent-flow.md)
- [Database Documentation](/docs/db/README.md)
