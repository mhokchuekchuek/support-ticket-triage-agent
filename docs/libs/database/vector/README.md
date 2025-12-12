# Vector Store

Vector database implementations using the provider/selector pattern.

## Location

`libs/database/vector/`

## Providers

| Provider | Description | Documentation |
|----------|-------------|---------------|
| `qdrant` | Qdrant vector database | [qdrant.md](qdrant.md) |

## Classes

### BaseVectorStore

Abstract base class for vector databases.

**Location**: `libs/database/vector/base.py`

**Methods**:

| Method | Description |
|--------|-------------|
| `add(**kwargs)` | Add embeddings to the store |
| `search(**kwargs)` | Search for similar embeddings |
| `delete(**kwargs)` | Delete embeddings |

### VectorStoreSelector

Selector for vector store providers.

**Location**: `libs/database/vector/selector.py`

**Methods**:

| Method | Description |
|--------|-------------|
| `create(provider, **kwargs)` | Create vector store instance |
| `list_providers()` | List available providers |
