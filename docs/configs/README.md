# Configuration Management

Dynaconf-based configuration management with YAML config files.

## Structure

```
configs/
├── agents/
│   └── triage.yaml         # Triage agent settings
├── litellm/
│   └── proxy_config.yaml   # LiteLLM proxy server config
└── vectordb.yaml           # Shared vector database settings
```

## Modules

| Module | Description |
|--------|-------------|
| [Settings](settings.md) | Settings class with Dynaconf integration |
| [Agents](agents/README.md) | Agent-specific configurations |
| [VectorDB](vectordb.md) | Shared vector database settings |
| [LiteLLM](litellm.md) | LiteLLM proxy server configuration |

## Quick Start

```python
from src.configs.settings import Settings

settings = Settings()

# Access nested config
settings.triage.llm.model       # "gpt-4o-mini"
settings.vectordb.host          # "localhost"
```

## Environment Variable Overrides

Override any config value via environment variables using `__` separator:

```bash
TRIAGE__LLM__MODEL=gpt-4o
VECTORDB__HOST=production.qdrant.io
```
