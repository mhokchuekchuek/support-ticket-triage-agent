# Langfuse Observability

Langfuse client for LLM tracing and monitoring.

**SDK Version**: Langfuse Python SDK v3 (OpenTelemetry-based)

## Location

`libs/llm/observability/langfuse/main.py`

## Class

### `LangfuseObservability`

Langfuse client for LLM observability and tracing.

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `public_key` | str | `LANGFUSE_PUBLIC_KEY` env | Langfuse public key |
| `secret_key` | str | `LANGFUSE_SECRET_KEY` env | Langfuse secret key |
| `host` | str | `https://cloud.langfuse.com` | Langfuse host URL |
| `enabled` | bool | `True` | Enable/disable observability |

## Methods

### `is_available() -> bool`

Check if Langfuse is available and connected.

### `get_callback_handler(session_id, user_id, metadata) -> CallbackHandler`

Get LangChain callback handler for automatic tracing.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `session_id` | str | Session ID for grouping traces |
| `user_id` | str | User ID for attribution |
| `metadata` | dict | Additional metadata |

### `trace_generation(name, input_data, output, model, metadata, session_id) -> Any`

Manually trace an LLM generation.

### `flush()`

Flush pending traces to Langfuse.

## Usage

```python
from libs.llm.observability.selector import ObservabilitySelector

# Create observability client
obs = ObservabilitySelector.create(
    provider="langfuse",
    public_key="pk-lf-...",
    secret_key="sk-lf-...",
    host="https://cloud.langfuse.com"
)

# Automatic tracing with LangGraph
# Use customer_id as session_id to group all customer interactions
handler = obs.get_callback_handler(
    session_id="customer_001",
    metadata={"ticket_id": "ticket_123", "plan": "enterprise"}
)
result = agent.invoke(input, config={"callbacks": [handler] if handler else []})

# Manual tracing
obs.trace_generation(
    name="embedding",
    input_data={"texts": texts},
    output=str(len(embeddings)),
    model="text-embedding-3-large"
)

# Flush traces
obs.flush()
```

## Environment Variables

```bash
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://cloud.langfuse.com
```
