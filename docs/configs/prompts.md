# Prompts Configuration

Prompt uploader settings for syncing prompts to Langfuse.

## Location

`configs/prompts.yaml`

## Configuration

```yaml
# Prompt Manager - Langfuse
prompt_manager:
  langfuse:
    enabled: true
    provider: langfuse
    host: "@jinja {{ env.get('LANGFUSE_HOST', 'https://cloud.langfuse.com') }}"
    public_key: "@format {env[LANGFUSE_PUBLIC_KEY]}"
    secret_key: "@format {env[LANGFUSE_SECRET_KEY]}"

# Prompts settings
prompts:
  directory: prompts
  version: v1
  label: production
```

## Parameters

### Prompt Manager

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompt_manager.langfuse.enabled` | bool | `true` | Enable Langfuse prompt manager |
| `prompt_manager.langfuse.provider` | string | `"langfuse"` | Provider name |
| `prompt_manager.langfuse.host` | string | `"https://cloud.langfuse.com"` | Langfuse host URL |
| `prompt_manager.langfuse.public_key` | string | - | Langfuse public key (from env) |
| `prompt_manager.langfuse.secret_key` | string | - | Langfuse secret key (from env) |

### Prompts

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `prompts.directory` | string | `"prompts"` | Directory containing .prompt files |
| `prompts.version` | string | `"v1"` | Version tag for uploaded prompts |
| `prompts.label` | string | `"production"` | Label for uploaded prompts |

## Usage

```python
from libs.configs.selector import ConfigSelector

settings = ConfigSelector.create(provider="dynaconf")

settings.prompts.directory                      # "prompts"
settings.prompts.version                        # "v1"
settings.prompt_manager.langfuse.provider       # "langfuse"
```

## Environment Variables

```bash
# Required for Langfuse authentication
LANGFUSE_PUBLIC_KEY=pk-lf-xxx
LANGFUSE_SECRET_KEY=sk-lf-xxx
LANGFUSE_HOST=https://cloud.langfuse.com
```
