# Configuration Management

Dynaconf-based configuration management with YAML config files.

## Structure

```
configs/
├── agents/
│   ├── shared.yaml         # Shared agent config (vectordb, observability, prompt_manager)
│   └── triage.yaml         # Triage agent settings
├── litellm/
│   └── proxy_config.yaml   # LiteLLM proxy server config
├── ingestor.yaml           # KB ingestor settings (includes vectordb)
└── prompts.yaml            # Prompts uploader settings
```

## Modules

| Module | Description |
|--------|-------------|
| [Agents](agents/README.md) | Agent-specific configurations |
| [Ingestor](ingestor.md) | KB ingestor settings |
| [Prompts](prompts.md) | Prompts uploader settings |
| [LiteLLM](litellm.md) | LiteLLM proxy server configuration |

## Settings Manager

See [libs/configs/dynaconf](../libs/configs/dynaconf.md) for configuration manager documentation.

## Quick Start

```python
from libs.configs.selector import ConfigSelector

settings = ConfigSelector.create(provider="dynaconf")

# Access nested config
settings.triage.llm.model                    # "gpt-4o-mini"
settings.agent_shared.vectordb.host          # "localhost"
settings.ingestor.vectordb.host              # "localhost"
settings.prompts.directory                   # "prompts"
```
