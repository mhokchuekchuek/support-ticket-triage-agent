# Shared Agent Configuration

Shared services and settings for all agents.

## Location

`configs/agents/shared.yaml`

## Configuration

```yaml
agent_shared:
  vectordb:
    provider: qdrant
    host: localhost
    port: 6333

  observability:
    langfuse:
      enabled: true
      provider: langfuse
      host: https://cloud.langfuse.com
      public_key: PLEASE REPLACE IN .ENV
      private_key: PLEASE REPLACE IN .ENV

  prompt_manager:
    langfuse:
      enabled: true
      provider: langfuse
    version: latest
    label: production
```

## Parameters

### Vector Database

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `vectordb.provider` | string | `"qdrant"` | Vector database provider |
| `vectordb.host` | string | `"localhost"` | Vector database host |
| `vectordb.port` | int | `6333` | Vector database port |

### Observability

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `observability.langfuse.enabled` | bool | `true` | Enable Langfuse tracing |
| `observability.langfuse.provider` | string | `"langfuse"` | Observability provider |
| `observability.langfuse.host` | string | `"https://cloud.langfuse.com"` | Langfuse host URL |
| `observability.langfuse.public_key` | string | - | Langfuse public key (set via .env) |
| `observability.langfuse.private_key` | string | - | Langfuse private key (set via .env) |

### Prompt Manager

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt_manager.langfuse.enabled` | bool | `true` | Enable Langfuse prompts |
| `prompt_manager.langfuse.provider` | string | `"langfuse"` | Prompt manager provider |
| `prompt_manager.version` | string | `"latest"` | Prompt version to fetch |
| `prompt_manager.label` | string | `"production"` | Prompt label to fetch |

## Usage

```python
from libs.configs.selector import ConfigSelector

settings = ConfigSelector.create(provider="dynaconf")

settings.agent_shared.vectordb.host                    # "localhost"
settings.agent_shared.observability.langfuse.enabled   # True
settings.agent_shared.prompt_manager.version           # "latest"
```

## Environment Overrides

```bash
AGENT_SHARED__VECTORDB__HOST=production.qdrant.io
AGENT_SHARED__VECTORDB__PORT=6333
AGENT_SHARED__OBSERVABILITY__LANGFUSE__ENABLED=false
AGENT_SHARED__OBSERVABILITY__LANGFUSE__PUBLIC_KEY=pk-lf-...
AGENT_SHARED__OBSERVABILITY__LANGFUSE__PRIVATE_KEY=sk-lf-...
AGENT_SHARED__PROMPT_MANAGER__VERSION=v2
```
