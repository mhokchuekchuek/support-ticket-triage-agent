# Ticket Matcher Agent Tools

LangChain tools for the TicketMatcherAgent.

## Location

`src/modules/agents/ticket_matcher/tools/`

## Tools

| Tool | File | Description |
|------|------|-------------|
| `TicketSummarizeTool` | `ticket_summarize.py` | Summarize ticket from Redis checkpoint |

## TicketSummarizeTool

Reads LangGraph checkpoint data from Redis and creates a summary for ticket matching.

```python
from src.modules.agents.ticket_matcher.tools.ticket_summarize import TicketSummarizeTool

summarize_tool = TicketSummarizeTool(kv_client=redis_client)
```

Returns: ticket type, urgency, current stage, last message preview

## See Also

- [TicketMatcherAgent](../README.md)
- [TicketSummarizeTool Details](ticket_summarize.md)
