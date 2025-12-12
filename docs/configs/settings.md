# Settings

Application settings manager using Dynaconf.

## Location

`src/configs/settings.py`

## Class

### `Settings`

**Example**:
```python
from src.configs.settings import Settings

settings = Settings()

# Access nested config
model = settings.triage.llm.model           # "gpt-4o-mini"
temperature = settings.triage.llm.temperature  # 0.7
host = settings.vectordb.host               # "localhost"

# Use .get() for optional values with defaults
log_level = settings.get("LOG_LEVEL", "INFO")
```

## How It Works

1. **Auto-discovery**: Auto-discovers all `*.yaml` files in `configs/` directory
2. **Exclusion**: `proxy_config.yaml` is excluded (used by LiteLLM proxy server directly)
3. **Merge**: All config files are merged into a single settings object
4. **Environment**: `.env` file is loaded automatically
5. **Override**: Environment variables override YAML values using `__` separator

## Environment Variable Overrides

| Environment Variable | Config Path |
|---------------------|-------------|
| `TRIAGE__LLM__MODEL` | `settings.triage.llm.model` |
| `TRIAGE__LLM__TEMPERATURE` | `settings.triage.llm.temperature` |
| `VECTORDB__HOST` | `settings.vectordb.host` |
| `VECTORDB__PORT` | `settings.vectordb.port` |
