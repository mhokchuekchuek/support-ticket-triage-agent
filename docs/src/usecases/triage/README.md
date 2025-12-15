# TriageService

Ticket triage use case - application business logic orchestration.

## Overview

`TriageService` handles the complete ticket triage lifecycle:

- Pre-workflow ticket matching
- Agent workflow execution
- Post-workflow persistence

## Location

`src/usecases/triage/main.py`

## Class Definition

```python
class TriageService:
    def __init__(
        self,
        workflow: MultiAgentWorkflow,
        checkpoint_repo: CheckpointRepository,
        ticket_repo: TicketRepository,
        chat_repo: ChatRepository,
        ticket_matcher_agent: Optional[BaseAgent] = None,
        ticket_summarize_tool: Optional[BaseTool] = None,
    ):
```

## Dependencies

| Dependency | Type | Purpose |
|------------|------|---------|
| workflow | MultiAgentWorkflow | Agent graph execution |
| checkpoint_repo | CheckpointRepository | Redis/checkpoint operations |
| ticket_repo | TicketRepository | SQL ticket persistence |
| chat_repo | ChatRepository | SQL chat message persistence |
| ticket_matcher_agent | BaseAgent (optional) | Match messages to activated tickets |
| ticket_summarize_tool | BaseTool (optional) | Summarize activated tickets |

## Main Method

### `triage_ticket(ticket, config) -> dict`

Execute full triage flow on a ticket.

**Flow:**

```
1. PRE-WORKFLOW
   ├── Scan activated tickets for customer
   ├── Summarize activated tickets
   └── Match incoming message to activated ticket

2. WORKFLOW
   └── Run agent graph (translator → supervisor → specialist)

3. POST-WORKFLOW
   ├── If AUTO_RESPOND or ESCALATE_HUMAN:
   │   ├── Save ticket to PostgreSQL
   │   ├── Save messages to PostgreSQL
   │   └── Delete Redis checkpoints
   └── If ROUTE_SPECIALIST:
       └── Keep activated in Redis
```

**Parameters:**
- `ticket`: Ticket entity to triage
- `config`: Optional workflow configuration

**Returns:**
- Workflow result dict containing `triage_result` and `messages`

## Private Methods

| Method | Purpose |
|--------|---------|
| `_resolve_ticket_id` | Match to activated ticket or generate new ID |
| `_get_ticket_summaries` | Get summaries for activated tickets |
| `_match_ticket` | Match message to activated ticket |
| `_build_config` | Build workflow config with thread_id |
| `_handle_persistence` | Persist completed or keep activated |
| `_persist_ticket` | Save to PostgreSQL, cleanup Redis |
| `_generate_ticket_id` | Generate new ticket ID (TKT-XXXXXXXX) |

## Persistence Logic

| RecommendedAction | Ticket State | Action |
|-------------------|--------------|--------|
| AUTO_RESPOND | Completed | Persist to PostgreSQL, delete Redis |
| ESCALATE_HUMAN | Completed | Persist to PostgreSQL, delete Redis |
| ROUTE_SPECIALIST | Activated | Keep in Redis for follow-up |

## Usage

```python
from src.usecases.triage.main import TriageService
from src.entities.ticket import Ticket

service = TriageService(
    workflow=workflow,
    checkpoint_repo=checkpoint_repo,
    ticket_repo=ticket_repo,
    chat_repo=chat_repo,
    ticket_matcher_agent=matcher_agent,
    ticket_summarize_tool=summarize_tool,
)

ticket = Ticket(
    customer_id="CUST-001",
    messages=[Message(content="I have a billing issue")],
)

result = service.triage_ticket(ticket)
triage_result = result["triage_result"]
```
