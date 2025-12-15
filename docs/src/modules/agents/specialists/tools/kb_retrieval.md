# KBRetrievalTool

Search the knowledge base for relevant articles with optional category filtering.

## Location

`src/modules/agents/specialists/tools/kb_retrieval.py`

## Classes

### `KBRetrievalInput`

Input schema for the tool.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `query` | str | Required | Search query for knowledge base |
| `top_k` | int | 3 | Number of results to return |

### `KBRetrievalTool`

LangChain tool for searching the knowledge base.

**Attributes**:

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | str | "kb_search" |
| `description` | str | Tool description for LLM |
| `vector_store` | BaseVectorStore | Qdrant client for search |
| `llm` | BaseLLM | LLM client for embeddings |
| `category_filter` | Optional[str] | Category to filter results by |

## Constructor

```python
KBRetrievalTool(
    vector_store: BaseVectorStore,
    llm: BaseLLM,
    category_filter: Optional[str] = None,
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `vector_store` | BaseVectorStore | Required | Vector store client |
| `llm` | BaseLLM | Required | LLM client with embed() method |
| `category_filter` | Optional[str] | None | Filter by category metadata |

## Methods

### `_run(query, top_k) -> str`

Execute KB search.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | str | Search query string |
| `top_k` | int | Number of results (default: 3) |

**Returns**: Formatted string with relevant KB articles.

## Category Filtering

Each specialist agent uses category filtering:

| Agent | Category Filter |
|-------|-----------------|
| BillingAgent | `billing` |
| TechnicalAgent | `technical` |
| GeneralAgent | `general` |

KB articles must have `category` in metadata:

```yaml
---
id: kb-001
title: Payment Failed
category: billing
---
```

## Usage

```python
from src.modules.agents.specialists.tools.kb_retrieval import KBRetrievalTool

# Without category filter (searches all)
tool = KBRetrievalTool(
    vector_store=vector_store,
    llm=llm,
)

# With category filter (billing only)
billing_tool = KBRetrievalTool(
    vector_store=vector_store,
    llm=llm,
    category_filter="billing",
)

# Direct call
result = billing_tool._run(query="payment failed", top_k=3)
```

## See Also

- [BillingAgent](../billing/README.md)
- [TechnicalAgent](../technical/README.md)
- [GeneralAgent](../general/README.md)
