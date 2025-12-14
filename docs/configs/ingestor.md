# Ingestor Configuration

Knowledge base ingestion pipeline settings.

## Location

`configs/ingestor.yaml`

## Configuration

```yaml
ingestor:
  kb_path: "data/knowledge_base"
  vectordb:
    provider: qdrant
    host: localhost
    port: 6333
    collection_name: knowledge_base
  embedding:
    model: "text-embedding-3-large"
    vector_size: 3072
  chunking:
    chunk_size: 32000
    chunk_overlap: 200
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `kb_path` | string | `"data/knowledge_base"` | Path to markdown knowledge base directory |
| `vectordb.provider` | string | `"qdrant"` | Vector database provider |
| `vectordb.host` | string | `"localhost"` | Vector database host |
| `vectordb.port` | int | `6333` | Vector database port |
| `vectordb.collection_name` | string | `"knowledge_base"` | Qdrant collection name |
| `embedding.model` | string | `"text-embedding-3-large"` | OpenAI embedding model |
| `embedding.vector_size` | int | `3072` | Embedding vector dimension |
| `chunking.chunk_size` | int | `32000` | Max characters per chunk (~8191 tokens) |
| `chunking.chunk_overlap` | int | `200` | Overlap between chunks |

## Usage

```python
from libs.configs.selector import ConfigSelector

settings = ConfigSelector.create(provider="dynaconf")

settings.ingestor.kb_path                      # "data/knowledge_base"
settings.ingestor.vectordb.provider            # "qdrant"
settings.ingestor.vectordb.host                # "localhost"
settings.ingestor.vectordb.port                # 6333
settings.ingestor.vectordb.collection_name     # "knowledge_base"
settings.ingestor.embedding.model              # "text-embedding-3-large"
settings.ingestor.embedding.vector_size        # 3072
settings.ingestor.chunking.chunk_size          # 32000
settings.ingestor.chunking.chunk_overlap       # 200
```

## Environment Overrides

```bash
INGESTOR__KB_PATH=custom/path
INGESTOR__VECTORDB__PROVIDER=qdrant
INGESTOR__VECTORDB__HOST=production.qdrant.io
INGESTOR__VECTORDB__PORT=6333
INGESTOR__VECTORDB__COLLECTION_NAME=my_collection
INGESTOR__EMBEDDING__MODEL=text-embedding-3-small
INGESTOR__EMBEDDING__VECTOR_SIZE=1536
INGESTOR__CHUNKING__CHUNK_SIZE=16000
INGESTOR__CHUNKING__CHUNK_OVERLAP=100
```
