# SpecialistBaseAgent

Base class for specialist agents (billing, technical, general).

## Location

`src/modules/agents/specialist_base.py`

## Class

### `SpecialistBaseAgent`

Provides shared functionality for all specialist agents.

**Class Attributes**:

| Attribute | Type | Description |
|-----------|------|-------------|
| `AGENT_NAME` | str | Name for logging |
| `PROMPT_ID` | str | Default Langfuse prompt ID |
| `DOMAIN` | str | Domain category |

**Instance Attributes**:

| Attribute | Type | Description |
|-----------|------|-------------|
| `llm` | BaseLLM | LLM client |
| `tools` | list | Tools (kb_search) |
| `observability` | LangfuseObservability | Observability for tracing |
| `prompt_manager` | BasePromptManager | Prompt management |
| `prompt_obj` | Prompt | Langfuse prompt object |
| `agent` | Agent | LangChain agent |

## Methods

### `execute(state: AgentState) -> AgentState`

Execute specialist triage.

### `_load_prompt() -> Prompt`

Load prompt object from prompt_manager.

### `_compile_prompt(ticket, translation, supervisor_decision) -> str`

Compile Langfuse prompt with ticket variables.

### `_parse_triage_result(output, supervisor_decision, translation) -> TriageResult`

Parse agent output into TriageResult.

## Subclassing

```python
class BillingAgent(SpecialistBaseAgent):
    AGENT_NAME = "BillingAgent"
    PROMPT_ID = "triage_billing"
    DOMAIN = "billing"
```

## Prompt Variables

| Variable | Description |
|----------|-------------|
| `ticket_content` | Ticket messages |
| `customer_info` | Customer details |
| `urgency` | From supervisor |
| `supervisor_reasoning` | Classification reasoning |
| `original_language` | For response generation |
