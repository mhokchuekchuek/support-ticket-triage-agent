# BaseAgent

Abstract base class for all agents in the triage system.

## Location

`src/modules/agents/base.py`

## Class

### `BaseAgent`

Abstract base class that all agents should inherit from.

**Attributes**:

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | str | Unique identifier for this agent |
| `logger` | Logger | Logger instance for this agent |

## Methods

### `__init__(name: str)`

Initialize the agent.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | str | Unique identifier for this agent |

### `execute(state: dict) -> dict` (abstract)

Execute the agent's logic on the current state.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `state` | dict[str, Any] | Current agent state with messages, ticket, etc. |

**Returns**: Updated agent state after processing.

## Usage

```python
from src.modules.agents.base import BaseAgent
from typing import Any


class BillingAgent(BaseAgent):
    """Agent that handles billing-related tickets."""

    def __init__(self, llm_client):
        super().__init__(name="billing")
        self.llm_client = llm_client

    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        self.logger.info(f"Processing ticket: {state.get('ticket_id')}")

        # Perform billing analysis
        result = self._analyze_ticket(state)

        # Update state
        state["triage_result"] = result
        return state

    def _analyze_ticket(self, state: dict) -> dict:
        # Implementation
        pass
```
