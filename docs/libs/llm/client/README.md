# LLM Client

LLM client implementations using the provider/selector pattern.

## Location

`libs/llm/client/`

## Providers

| Provider | Description | Documentation |
|----------|-------------|---------------|
| `litellm` | HTTP-based LiteLLM proxy client | [litellm.md](litellm.md) |
| `langchain` | LangChain ChatOpenAI wrapper | [langchain.md](langchain.md) |

## Classes

### BaseLLM

Abstract base class for LLM clients.

**Location**: `libs/llm/client/base.py`

**Methods**:

| Method | Description |
|--------|-------------|
| `generate(prompt, system_prompt, **kwargs)` | Generate text completion |
| `embed(texts, **kwargs)` | Generate embeddings |

### LLMClientSelector

Selector for LLM client providers.

**Location**: `libs/llm/client/selector.py`

**Methods**:

| Method | Description |
|--------|-------------|
| `create(provider, **kwargs)` | Create client instance |
| `list_providers()` | List available providers |
