# SupervisorAgent

Agent responsible for classifying ticket urgency/type and routing to specialist agents.

## Location

`src/modules/agents/supervisor.py`

## Class

### `SupervisorAgent`

Analyzes translated tickets to determine urgency level, ticket type, and routes to the appropriate specialist agent.

**Attributes**:

| Attribute | Type | Description |
|-----------|------|-------------|
| `llm` | BaseLLM | LLM client for reasoning |
| `tools` | list | Tools available (customer_lookup) |
| `observability` | LangfuseObservability | Observability wrapper for tracing |
| `prompt_manager` | BasePromptManager | Prompt manager for loading prompts |
| `agent_config` | dict | Agent configuration from YAML |
| `system_prompt` | str | Loaded from prompt_manager |
| `agent` | Agent | LangChain agent instance |

## Methods

### `execute(state: AgentState) -> AgentState`

Classify ticket and decide routing.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `state` | AgentState | Current state with ticket and translation |

**Returns**: Updated state with `supervisor_decision` field containing `SupervisorDecision`.

## Tools

- **customer_lookup**: Retrieves customer information by ID

## Configuration

```yaml
triage:
  agents:
    supervisor:
      prompt:
        id: triage_supervisor
        environment: production
```

## Output

Adds `SupervisorDecision` to state:

```python
SupervisorDecision(
    urgency=UrgencyLevel.HIGH,
    ticket_type=TicketType.BILLING,
    reasoning="Customer reports payment failure...",
    requires_escalation=False
)
```

## Routing Logic

| Ticket Type | Routes To |
|-------------|-----------|
| billing | BillingAgent |
| technical | TechnicalAgent |
| general | GeneralAgent |
| requires_escalation=True | Direct escalation |
