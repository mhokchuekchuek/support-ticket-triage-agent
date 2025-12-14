# Dynaconf Provider

Dynaconf-based configuration manager with YAML files and environment variable support.

## Location

`libs/configs/dynaconf/main.py`

## Usage

```python
from libs.configs.selector import ConfigSelector

# Auto-detect project root
settings = ConfigSelector.create(provider="dynaconf")

# With explicit configuration
settings = ConfigSelector.create(
    provider="dynaconf",
    project_root="/path/to/project",
    configs_dir="configs",
    env_file=".env"
)
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `project_root` | `str \| Path \| None` | Auto-detect | Project root directory |
| `configs_dir` | `str \| Path` | `"configs"` | Config files directory |
| `env_file` | `str \| Path` | `".env"` | Environment file path |
| `exclude_patterns` | `list[str]` | `["proxy_config"]` | Files to exclude |
| `envvar_prefix` | `str \| bool` | `False` | Env var prefix |
| `environments` | `bool` | `False` | Enable Dynaconf environments |
| `nested_separator` | `str` | `"__"` | Separator for nested env vars |
| `merge_enabled` | `bool` | `True` | Merge nested config dicts |

## Auto-detection

When `project_root` is not specified, auto-detects by looking for:
- `.git`
- `pyproject.toml`
- `setup.py`
- `setup.cfg`
- `requirements.txt`

## Environment Variable Interpolation

Reference env vars directly in YAML config files.

### Without Default Value

Use `@format` syntax:

```yaml
api_key: "@format {env[OPENAI_API_KEY]}"
secret: "@format {env[LANGFUSE_SECRET_KEY]}"
```

### With Default Value

Use `@jinja` syntax:

```yaml
host: "@jinja {{ env.get('DB_HOST', 'localhost') }}"
port: "@jinja {{ env.get('DB_PORT', '5432') }}"
```

### Example

```yaml
# configs/agents/shared.yaml
agent_shared:
  observability:
    langfuse:
      enabled: true
      host: "@jinja {{ env.get('LANGFUSE_HOST', 'https://cloud.langfuse.com') }}"
      public_key: "@format {env[LANGFUSE_PUBLIC_KEY]}"
      secret_key: "@format {env[LANGFUSE_SECRET_KEY]}"
```

## Environment Variable Overrides

Override any config value via environment variables using `__` separator:

```bash
TRIAGE__LLM__MODEL=gpt-4o
AGENT_SHARED__VECTORDB__HOST=production.qdrant.io
```
