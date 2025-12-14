# AgentState

State TypedDict for the multi-agent triage workflow.

## Location

`src/modules/graph/state.py`

## Enums

### `TicketType`

Ticket classification type for routing.

| Value | Description |
|-------|-------------|
| `BILLING` | Billing-related issues |
| `TECHNICAL` | Technical/system issues |
| `GENERAL` | General inquiries |

## Models

### `TranslationResult`

Result from TranslatorAgent.

| Field | Type | Description |
|-------|------|-------------|
| `original_language` | str | Detected language code |
| `is_english` | bool | Whether ticket is in English |
| `translated_messages` | Optional[list[str]] | Translated messages (if non-English) |
| `original_messages` | list[str] | Original message content |

### `SupervisorDecision`

Routing decision from SupervisorAgent.

| Field | Type | Description |
|-------|------|-------------|
| `urgency` | UrgencyLevel | Classified urgency |
| `ticket_type` | TicketType | Classified type for routing |
| `reasoning` | str | Classification reasoning |
| `requires_escalation` | bool | Direct escalation flag |

## Classes

### `AgentState`

TypedDict defining state passed between workflow nodes.

| Field | Type | Description |
|-------|------|-------------|
| `messages` | Annotated[list[BaseMessage], add_messages] | Message history with auto-accumulation |
| `ticket` | Ticket | Input ticket being processed |
| `customer_info` | Optional[dict] | Customer info from lookup |
| `kb_results` | Optional[list[dict]] | KB search results |
| `triage_result` | Optional[TriageResult] | Final triage result |
| `iteration` | int | Iteration counter for loop control |
| `translation` | Optional[TranslationResult] | Translation result from TranslatorAgent |
| `supervisor_decision` | Optional[SupervisorDecision] | Routing decision from SupervisorAgent |
| `current_agent` | Optional[str] | Currently executing agent name |

## Functions

### `create_initial_state(ticket) -> AgentState`

Create initial workflow state from a ticket.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `ticket` | Ticket | Support ticket to process |

**Returns**: AgentState with ticket set and other fields initialized.

## Usage

```python
from src.modules.graph.state import AgentState, create_initial_state
from src.entities.ticket import Ticket

ticket = Ticket(...)
state = create_initial_state(ticket)

# Access state fields
state["ticket"]        # Ticket
state["messages"]      # []
state["triage_result"] # None
```
