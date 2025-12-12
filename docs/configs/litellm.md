# LiteLLM Proxy Configuration

LiteLLM proxy server configuration for centralized LLM management.

## Location

`configs/litellm/proxy_config.yaml`

## Configuration

```yaml
model_list:
  - model_name: gpt-4o-mini
    litellm_params:
      model: openai/gpt-4o-mini
      api_key: os.environ/OPENAI_API_KEY

  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY

  - model_name: text-embedding-3-small
    litellm_params:
      model: text-embedding-3-small
      api_key: os.environ/OPENAI_API_KEY

litellm_settings:
  cache: false
  num_retries: 3
  request_timeout: 600
  drop_params: true

general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: os.environ/DATABASE_URL
  health_check: true
  health_check_interval: 300

router_settings:
  routing_strategy: simple-shuffle
```

## Parameters

### Model List

| Parameter | Type | Description |
|-----------|------|-------------|
| `model_name` | string | Alias name for the model |
| `litellm_params.model` | string | Provider/model identifier |
| `litellm_params.api_key` | string | API key (use `os.environ/VAR_NAME`) |

### LiteLLM Settings

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `cache` | bool | `false` | Enable response caching |
| `num_retries` | int | `3` | Number of retry attempts |
| `request_timeout` | int | `600` | Request timeout in seconds |
| `drop_params` | bool | `true` | Drop unsupported params instead of erroring |

### General Settings

| Parameter | Type | Description |
|-----------|------|-------------|
| `master_key` | string | API authentication key |
| `database_url` | string | Database connection URL |
| `health_check` | bool | Enable health check endpoint |
| `health_check_interval` | int | Health check interval in seconds |

### Router Settings

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `routing_strategy` | string | `simple-shuffle` | Load balancing strategy |

## Documentation

- [LiteLLM Proxy Configs](https://docs.litellm.ai/docs/proxy/configs)
