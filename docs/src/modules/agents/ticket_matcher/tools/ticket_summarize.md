# TicketSummarizeTool

Summarize an active ticket from Redis checkpoint data for ticket matching.

## Location

`src/modules/agents/ticket_matcher/tools/ticket_summarize.py`

## Classes

### `TicketSummarizeInput`

Input schema for the tool.

| Field | Type | Description |
|-------|------|-------------|
| `ticket_id` | str | Ticket ID to summarize |
| `customer_id` | str | Customer ID |

### `TicketSummarizeTool`

LangChain tool for summarizing tickets from Redis checkpoints.

**Attributes**:

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | str | "ticket_summarize" |
| `description` | str | Tool description for LLM |
| `kv_client` | BaseKeyValueClient | Redis client |

## Constructor

```python
TicketSummarizeTool(kv_client: BaseKeyValueClient)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `kv_client` | BaseKeyValueClient | Key-value client for Redis |

## Methods

### `_run(ticket_id, customer_id) -> str`

Summarize ticket from Redis checkpoint.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `ticket_id` | str | Ticket ID to summarize |
| `customer_id` | str | Customer ID |

**Returns**: Formatted summary string.

### `_extract_summary(ticket_id, checkpoint) -> str`

Extract summary from checkpoint data.

Extracts from LangGraph `channel_values`:
- `supervisor_decision.ticket_type`
- `supervisor_decision.urgency`
- `ticket.messages[-1].content` (last message)
- `current_agent` (current workflow stage)

## Output Format

```
**Ticket TKT-ABC12345**
Type: technical
Urgency: high
Current Stage: technical
Last Message: Connection timeout error on API...
```

## Redis Key Pattern

```
*{customer_id}:{ticket_id}*
```

Example: `langgraph:checkpoint:cust_123:TKT-ABC12345:...`

## Usage

```python
from src.modules.agents.ticket_matcher.tools.ticket_summarize import TicketSummarizeTool

# Initialize with Redis client
summarize_tool = TicketSummarizeTool(kv_client=redis_client)

# Direct call
summary = summarize_tool._run(
    ticket_id="TKT-ABC12345",
    customer_id="cust_123"
)
```

## Error Handling

- Returns `"No checkpoint found for ticket {id}"` if no keys match
- Returns `"Could not parse checkpoint for ticket {id}"` if data invalid
- Returns `"Error summarizing ticket {id}: {error}"` on failure

## See Also

- [TicketMatcherAgent](../README.md)
- [Redis Checkpoint](/docs/libs/database/keyvalue_db/README.md)
- [AgentState](/docs/src/modules/graph/state.md)
