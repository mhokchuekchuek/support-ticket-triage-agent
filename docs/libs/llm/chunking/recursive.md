# Recursive Text Chunker

Text chunker using LangChain's RecursiveCharacterTextSplitter.

## Location

`libs/llm/chunking/recursive/main.py`

## Class

### `TextChunker`

Recursively splits text using a hierarchy of separators to preserve semantic boundaries.

**Split order**: paragraphs -> lines -> sentences -> words -> characters

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `chunk_size` | int | 512 | Target size for each chunk (characters) |
| `chunk_overlap` | int | 50 | Characters to overlap between chunks |
| `separators` | list[str] | None | Custom list of separators |

## Methods

### `split(text, metadata) -> list[dict]`

Split text into chunks.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | str | Text to split |
| `metadata` | dict | Optional metadata to attach to each chunk |

**Returns**: List of dicts containing:

```python
{
    "text": str,
    "metadata": {
        "chunk_index": int,
        "chunk_size": int,
        ...  # additional metadata passed in
    }
}
```

## Usage

```python
from libs.llm.chunking.selector import TextChunkerSelector

chunker = TextChunkerSelector.create(
    provider="recursive",
    chunk_size=1000,
    chunk_overlap=200
)

chunks = chunker.split(
    text="Long document text...",
    metadata={"source": "document.pdf"}
)

for chunk in chunks:
    print(f"Chunk {chunk['metadata']['chunk_index']}: {chunk['text'][:50]}...")
```
