# OpenAI Embeddings

## Problem

The knowledge base ingestor needs to convert text articles into vector embeddings for semantic search in Qdrant.

## Solution

We use [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings) via LiteLLM proxy because the assignment prefers OpenAI models throughout the project.

**Reference:** [OpenAI Embedding Models](https://platform.openai.com/docs/models/text-embedding-3-large)

## How It Works

Embeddings are generated through the LiteLLM proxy which routes to OpenAI's API.

**Reference:** [LiteLLM Embeddings](https://docs.litellm.ai/docs/embedding/supported_embedding)

### Code Example

```python
from libs.llm.client.selector import LLMClientSelector

client = LLMClientSelector.create(
    provider="litellm",
    proxy_url="http://localhost:4000",
    embedding_model="text-embedding-3-large",
)

embeddings = client.embed(["Your text here"])  # Returns list of 3072-dim vectors
```

## Available Models

| Model | Dimensions | Performance |
|-------|------------|-------------|
| `text-embedding-3-large` | 3072 | Best quality |
| `text-embedding-3-small` | 1536 | Cost-effective |
| `text-embedding-ada-002` | 1536 | Legacy |

## Configuration

See [`configs/ingestor.yaml`](../../configs/ingestor.yaml) for embedding settings.
