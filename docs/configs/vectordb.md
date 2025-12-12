# Vector Database Configuration

Shared vector database settings.

## Location

`configs/vectordb.yaml`

## Configuration

```yaml
vectordb:
  provider: "qdrant"
  host: "localhost"
  port: 6333
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `provider` | string | `"qdrant"` | Vector database provider |
| `host` | string | `"localhost"` | Database server hostname |
| `port` | int | `6333` | Database server port (REST API) |

## Usage

```python
from src.configs.settings import Settings

settings = Settings()

settings.vectordb.provider  # "qdrant"
settings.vectordb.host      # "localhost"
settings.vectordb.port      # 6333
```

## Environment Overrides

```bash
VECTORDB__HOST=production.qdrant.io
VECTORDB__PORT=6334
```
