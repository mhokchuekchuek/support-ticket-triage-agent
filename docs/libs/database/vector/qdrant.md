# Qdrant Vector Store

Qdrant vector database client with metadata filtering support.

## Location

`libs/database/vector/qdrant/main.py`

## Class

### `VectorStoreClient`

Qdrant vector database client with metadata support.

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `host` | str | `localhost` | Qdrant server host |
| `port` | int | 6333 | Qdrant server port |
| `collection_name` | str | `documents` | Collection name |
| `vector_size` | int | 1536 | Embedding vector dimension |
| `distance` | str | `Cosine` | Distance metric (Cosine, Euclid, Dot) |
| `create_collection` | bool | True | Create collection if not exists |

## Methods

### `add(embeddings, metadata, ids) -> None`

Add embeddings to Qdrant.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `embeddings` | list[list[float]] | List of embedding vectors |
| `metadata` | list[dict] | Optional metadata for each embedding |
| `ids` | list[str] | Optional IDs (auto-generated if not provided) |

### `search(query_embedding, k, filter) -> list[dict]`

Search for similar embeddings.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `query_embedding` | list[float] | Query vector |
| `k` | int | Number of results (default: 5) |
| `filter` | dict | Optional metadata filter |

**Returns**: List of results with id, score, metadata, text

### `delete(ids, filter) -> None`

Delete embeddings by ID or filter.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `ids` | list[str] | List of IDs to delete |
| `filter` | dict | Metadata filter for deletion |

### `count(filter) -> int`

Count points in collection (Qdrant-specific).

## Usage

```python
from libs.database.vector.selector import VectorStoreSelector

store = VectorStoreSelector.create(
    provider="qdrant",
    host="localhost",
    port=6333,
    collection_name="my_documents",
    vector_size=384
)

# Add embeddings
store.add(
    embeddings=[[0.1, 0.2, ...], [0.3, 0.4, ...]],
    metadata=[
        {"text": "Hello world", "source": "doc1.pdf"},
        {"text": "Goodbye world", "source": "doc2.pdf"}
    ]
)

# Search
results = store.search(
    query_embedding=[0.1, 0.2, ...],
    k=5,
    filter={"source": "doc1.pdf"}
)

# Delete by filter
store.delete(filter={"source": "doc1.pdf"})
```
