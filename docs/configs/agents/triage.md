# Triage Agent Configuration

Multi-agent triage system settings.

## Location

`configs/agents/triage.yaml`

## Configuration

```yaml
triage:
  llm:
    provider: "litellm"
    model: "gpt-4o-mini"
    embedding_model: "text-embedding-3-large"
    temperature: 0.7
    max_tokens: 2000

  vectordb:
    collection_name: "knowledge_base"

  agents:
    translator:
      prompt:
        id: triage_translator
        environment: production

    supervisor:
      prompt:
        id: triage_supervisor
        environment: production

    billing:
      prompt:
        id: triage_billing
        environment: production
      category_filter: billing

    technical:
      prompt:
        id: triage_technical
        environment: production
      category_filter: technical

    general:
      prompt:
        id: triage_general
        environment: production
      category_filter: general
```

## Parameters

### LLM Settings

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `provider` | string | `"litellm"` | LLM provider to use |
| `model` | string | `"gpt-4o-mini"` | Model name for completions |
| `embedding_model` | string | `"text-embedding-3-large"` | Model for embeddings |
| `temperature` | float | `0.7` | Sampling temperature (0.0-1.0) |
| `max_tokens` | int | `2000` | Maximum tokens in response |

### VectorDB Settings

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `collection_name` | string | `"knowledge_base"` | Qdrant collection name |

### Agent Settings

Each agent has:

| Parameter | Type | Description |
|-----------|------|-------------|
| `prompt.id` | string | Langfuse prompt name |
| `prompt.environment` | string | Langfuse prompt label |
| `category_filter` | string | KB category filter (specialists only) |

## Usage

```python
from libs.configs.base import BaseConfigManager

settings = BaseConfigManager()

# Access LLM config
settings.triage.llm.provider    # "litellm"
settings.triage.llm.model       # "gpt-4o-mini"

# Access agent configs
settings.triage.agents.translator.prompt.id  # "triage_translator"
settings.triage.agents.billing.category_filter  # "billing"
```

## Environment Overrides

```bash
TRIAGE__LLM__MODEL=gpt-4o
TRIAGE__AGENTS__BILLING__CATEGORY_FILTER=payments
```
