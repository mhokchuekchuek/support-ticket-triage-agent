# Ingestor Module

Knowledge base ingestion pipeline for processing markdown articles into Qdrant vector store.

## Overview

The ingestor module loads markdown files with YAML frontmatter from the knowledge base directory, generates embeddings using OpenAI, and stores them in Qdrant for semantic search.

## Components

| Component | Description |
|-----------|-------------|
| [KBProcessor](processor.md) | Main processor class for loading and ingesting articles |

## Usage

### Run Ingestion Script

```bash
python scripts/ingest_kb.py
```

### Programmatic Usage

```python
from ingestor.processor import KBProcessor
from src.configs.settings import Settings

settings = Settings()
processor = KBProcessor(settings=settings)
count = processor.process()
print(f"Ingested {count} articles")
```

## Knowledge Base Format

Articles are stored as markdown files with YAML frontmatter:

```
data/knowledge_base/
├── billing/
│   ├── kb_001_refund_process.md
│   └── kb_002_double_charge.md
├── technical/
│   └── kb_010_500_errors.md
└── ...
```

### Article Structure

```markdown
---
id: kb_001
title: How to Request a Refund
category: billing
keywords:
  - refund
  - money back
  - cancel
---

Article content goes here...
```

## Configuration

See [Ingestor Configuration](../configs/ingestor.md) for settings.

## Pipeline Flow

```mermaid
flowchart LR
    A[Markdown Files] --> B[Load Frontmatter]
    B --> C[Chunk Text]
    C --> D[Generate Embeddings]
    D --> E[Store in Qdrant]
```

1. **Load**: Scan `data/knowledge_base/**/*.md` files
2. **Parse**: Extract frontmatter metadata and content
3. **Chunk**: Split text using `RecursiveCharacterTextSplitter` (32000 chars max)
4. **Embed**: Generate embeddings via OpenAI `text-embedding-3-large`
5. **Store**: Upsert chunks into Qdrant `knowledge_base` collection

## Why Recursive Chunking?

We use `RecursiveCharacterTextSplitter` for text chunking because:

| Reason | Description |
|--------|-------------|
| **Semantic Boundaries** | Splits on natural boundaries (paragraphs → sentences → words) preserving meaning |
| **Token Limit** | `text-embedding-3-large` has 8191 token limit; chunking ensures texts fit |
| **Retrieval Quality** | Smaller, focused chunks improve semantic search accuracy |
| **Overlap** | 200 char overlap prevents context loss at chunk boundaries |

Our KB articles are short FAQ-style documents, so advanced chunking methods (semantic, LLM-based) are unnecessary. Recursive chunking is simple, fast, and sufficient for this use case.
