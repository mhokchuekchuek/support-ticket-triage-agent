# LiteLLM Client

HTTP-based client for LiteLLM proxy.

## Location

`libs/llm/client/litellm/main.py`

## Class

### `LLMClient`

LiteLLM proxy client using HTTP requests.

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `proxy_url` | str | `http://litellm-proxy:4000` | Proxy URL |
| `completion_model` | str | None | Model for completions |
| `embedding_model` | str | None | Model for embeddings |
| `temperature` | float | 0.7 | Sampling temperature |
| `max_tokens` | int | 2000 | Max response tokens |
| `api_key` | str | `dummy` | API key for proxy |
| `timeout` | float | 120.0 | Request timeout |

## Methods

### `generate(prompt, system_prompt, prompt_variables, **kwargs) -> str`

Generate text completion via proxy.

**Modes**:

1. **Traditional mode**: Direct prompt strings
2. **Dotprompt mode**: Template variables for .prompt files

**Examples**:

```python
# Traditional mode
response = client.generate(
    prompt="Hello",
    system_prompt="You are helpful"
)

# Dotprompt mode
response = client.generate(
    prompt_variables={"question": "What is RAG?", "context": "..."}
)
```

### `embed(texts, **kwargs) -> list[list[float]]`

Generate embeddings via proxy.

**Example**:

```python
embeddings = client.embed(["text1", "text2"])
```

## Usage

```python
from libs.llm.client.selector import LLMClientSelector

client = LLMClientSelector.create(
    provider="litellm",
    proxy_url="http://litellm-proxy:4000",
    completion_model="gpt-4o-mini",
    embedding_model="text-embedding-3-small",
    temperature=0.5
)

# Generate text
response = client.generate(
    prompt="What is machine learning?",
    system_prompt="You are a helpful assistant."
)

# Generate embeddings
embeddings = client.embed(["Hello world", "How are you?"])
```
