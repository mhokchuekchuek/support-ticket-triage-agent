# LangChain Client

LangChain ChatOpenAI wrapper for LiteLLM proxy.

## Location

`libs/llm/client/langchain/main.py`

## Class

### `LLMClient`

LangChain ChatOpenAI wrapper for LiteLLM proxy.

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `proxy_url` | str | `http://litellm-proxy:4000` | Proxy URL |
| `api_key` | str | `sk-1234` | API key for proxy |
| `default_model` | str | `gpt-4` | Default model |
| `default_temperature` | float | 0.7 | Default temperature |
| `default_max_tokens` | int | 2000 | Default max tokens |

## Methods

### `get_client(model, temperature, max_tokens, extra_body, **kwargs) -> ChatOpenAI`

Get ChatOpenAI instance configured for LiteLLM proxy.

**Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | str | Model name (defaults to default_model) |
| `temperature` | float | Sampling temperature |
| `max_tokens` | int | Maximum tokens |
| `extra_body` | dict | Extra body for LiteLLM (e.g., prompt_variables) |

**Returns**: Configured `ChatOpenAI` instance

## Usage

### Standard Mode (Agents)

```python
from libs.llm.client.selector import LLMClientSelector

client = LLMClientSelector.create(
    provider="langchain",
    proxy_url="http://litellm-proxy:4000",
    default_model="gpt-4o-mini"
)

# Get ChatOpenAI instance
chat = client.get_client(
    model="gpt-4o-mini",
    temperature=0.5,
    max_tokens=1000
)

# Use with LangGraph agent
from langgraph.prebuilt import create_react_agent
agent = create_react_agent(model=chat, tools=[...])
```

### Dotprompt Mode (Templates)

```python
chat = client.get_client(
    model="rag-dotprompt",
    extra_body={"prompt_variables": {"query": "What is RAG?"}}
)
response = chat.invoke([])
```
