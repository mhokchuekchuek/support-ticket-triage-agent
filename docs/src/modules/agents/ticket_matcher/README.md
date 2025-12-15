# TicketMatcherAgent

Agent for matching new messages to existing active tickets.

## Location

`src/modules/agents/ticket_matcher/`

## Structure

```
ticket_matcher/
├── __init__.py
├── main.py                     # TicketMatcherAgent
└── tools/
    ├── __init__.py
    └── ticket_summarize.py     # TicketSummarizeTool
```

## Overview

Runs before the main workflow to determine if a new customer message relates to an existing active ticket:
- Scans Redis for customer's active tickets
- Uses TicketSummarizeTool to get summaries from checkpoints
- Uses LLM to match new message against active ticket summaries
- Returns matched ticket_id or signals to create new ticket

## Class

```python
class TicketMatcherAgent(BaseAgent):
    AGENT_NAME = "ticket_matcher"

    def __init__(
        self,
        llm,
        observability: Optional[Any] = None,
        prompt_manager: Optional[Any] = None,
        agent_config: Optional[dict] = None,
    ):
        ...
```

## Tools

### TicketSummarizeTool

Reads LangGraph checkpoint from Redis and extracts key information for ticket matching.

**Location**: `src/modules/agents/ticket_matcher/tools/ticket_summarize.py`

```python
from src.modules.agents.ticket_matcher.tools.ticket_summarize import TicketSummarizeTool

tool = TicketSummarizeTool(kv_client=redis_client)
summary = tool._run(ticket_id="TKT-001", customer_id="CUST-001")
```

## Usage

```python
from src.modules.agents.ticket_matcher.main import TicketMatcherAgent
from src.modules.agents.ticket_matcher.tools.ticket_summarize import TicketSummarizeTool

summarize_tool = TicketSummarizeTool(kv_client=kv_client)

agent = TicketMatcherAgent(
    llm=llm,
    prompt_manager=prompt_manager,
    agent_config=config,
)

# Execute matching
state = agent.execute({
    "new_message": "Any update on my issue?",
    "active_tickets": [
        {"ticket_id": "TKT-001", "summary": "Billing dispute..."},
    ]
})
```

## Output

Returns `match_result` dict:
- `matched_ticket_id`: Matched ticket ID or None
- `confidence`: "high" / "medium" / "low"
- `reasoning`: Explanation of match decision

## Matching Logic

**Match to existing ticket when:**
- Message explicitly references the same issue
- Message is a follow-up question about the same topic
- Customer says "regarding my previous issue" or similar

**Create new ticket when:**
- Message is about a completely different topic
- No active tickets exist
- Confidence is low (when uncertain, prefer new ticket)

## See Also

- [BaseAgent](../base.md)
- [Agent Flow](../../graph/agent-flow.md)
- [Pre-Workflow Ticket Matching](../../graph/agent-flow.md#step-0-pre-workflow-ticket-matching)
