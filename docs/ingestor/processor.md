# KBProcessor

Main class for knowledge base processing and ingestion.

## Location

`ingestor/processor.py`

## Class Definition

```python
class KBProcessor:
    def __init__(self, settings: Settings | None = None): ...
    def load_knowledge_base(self) -> list[dict]: ...
    def process(self) -> int: ...
```

## Methods

### `__init__(settings)`

Initialize processor with application settings.

**Parameters:**
- `settings`: Optional Settings instance. Creates new one if not provided.

**Initializes:**
- Qdrant vector store client via `VectorStoreSelector`
- LiteLLM client for embeddings via `LLMClientSelector`
- Text chunker via `TextChunkerSelector` (recursive)

### `load_knowledge_base()`

Load all markdown articles from knowledge base directory.

**Returns:** List of article dicts with:
- `id`: Article identifier (e.g., `kb_001`)
- `title`: Article title
- `content`: Markdown content
- `category`: Category name
- `keywords`: List of keywords

**Raises:** `FileNotFoundError` if KB directory doesn't exist.

### `process()`

Main ingestion pipeline - load, chunk, embed, and store articles.

**Returns:** Number of successfully ingested chunks.

**Steps:**
1. Load articles via `load_knowledge_base()`
2. Combine title + content for each article
3. Chunk text using `TextChunkerSelector` (RecursiveCharacterTextSplitter)
4. Generate embeddings for each chunk via LiteLLM proxy
5. Store chunks in Qdrant with metadata

## Usage Example

```python
from ingestor.processor import KBProcessor
from src.configs.settings import Settings

# Initialize
settings = Settings()
processor = KBProcessor(settings=settings)

# Run ingestion
count = processor.process()
print(f"Ingested {count} chunks")
```

## Metadata Storage

Each chunk is stored in Qdrant with:

```python
{
    "article_id": "kb_001",
    "title": "Article title",
    "category": "billing",
    "keywords": ["refund", "payment"],
    "chunk_index": 0,
    "chunk_size": 1234,
    "text": "Chunk text..."
}
```

## Dependencies

- `frontmatter`: Parse markdown frontmatter
- `libs.llm.client.selector`: LiteLLM client for embeddings
- `libs.llm.chunking.selector`: Text chunker for splitting documents
- `libs.database.vector.selector`: Vector store access
- `src.configs.settings`: Configuration management
