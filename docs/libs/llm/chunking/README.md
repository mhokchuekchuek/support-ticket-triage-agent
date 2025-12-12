# Text Chunking

Text chunking strategies using the provider/selector pattern.

## Location

`libs/llm/chunking/`

## Providers

| Provider | Description | Documentation |
|----------|-------------|---------------|
| `recursive` | Recursive character text splitter | [recursive.md](recursive.md) |

## Classes

### BaseChunker

Abstract base class for text chunking strategies.

**Location**: `libs/llm/chunking/base.py`

**Methods**:

| Method | Description |
|--------|-------------|
| `split(text, metadata)` | Split text into chunks |

### TextChunkerSelector

Selector for text chunker providers.

**Location**: `libs/llm/chunking/selector.py`

**Methods**:

| Method | Description |
|--------|-------------|
| `create(provider, **kwargs)` | Create chunker instance |
| `list_providers()` | List available providers |
