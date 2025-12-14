# Configs Module

Configuration management using the provider/selector pattern.

## Location

`libs/configs/`

## Providers

| Provider | Description | Documentation |
|----------|-------------|---------------|
| `dynaconf` | Dynaconf-based config with YAML files and env var support | [dynaconf.md](dynaconf.md) |

## Classes

### BaseConfigManager

Abstract base class for configuration managers.

**Location**: `libs/configs/base.py`

**Methods**:

| Method | Description |
|--------|-------------|
| `get(key, default)` | Get config value with optional default |
| `as_dict()` | Get all config as dictionary |
| `__getattr__(name)` | Access config as attributes |

### ConfigSelector

Selector for configuration manager providers.

**Location**: `libs/configs/selector.py`

**Methods**:

| Method | Description |
|--------|-------------|
| `create(provider, **kwargs)` | Create config manager instance |
| `list_providers()` | List available providers |

## Usage

```python
from libs.configs.selector import ConfigSelector

# Create with auto-detected project root
settings = ConfigSelector.create(provider="dynaconf")

# Access configuration
settings.triage.llm.model           # "gpt-4o-mini"
settings.get("LOG_LEVEL", "INFO")   # With default
```
