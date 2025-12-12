# Triage Agent Configuration

Support ticket triage agent settings.

## Location

`configs/agents/triage.yaml`

## Configuration

```yaml
triage:
  llm:
    provider: "litellm"
    model: "gpt-4o-mini"
    temperature: 0.7
    max_tokens: 2000

  vectordb:
    collection_name: "knowledge_base"
```

## Parameters

### LLM Settings

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `provider` | string | `"litellm"` | LLM provider to use |
| `model` | string | `"gpt-4o-mini"` | Model name for completions |
| `temperature` | float | `0.7` | Sampling temperature (0.0-1.0) |
| `max_tokens` | int | `2000` | Maximum tokens in response |

### VectorDB Settings

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `collection_name` | string | `"knowledge_base"` | Qdrant collection for this agent |

## Usage

```python
from src.configs.settings import Settings

settings = Settings()

# Access LLM config
settings.triage.llm.provider    # "litellm"
settings.triage.llm.model       # "gpt-4o-mini"
settings.triage.llm.temperature # 0.7
settings.triage.llm.max_tokens  # 2000

# Access agent-specific collection
settings.triage.vectordb.collection_name  # "knowledge_base"
```

## Environment Overrides

```bash
TRIAGE__LLM__MODEL=gpt-4o
TRIAGE__LLM__TEMPERATURE=0.5
TRIAGE__VECTORDB__COLLECTION_NAME=support_tickets
```
