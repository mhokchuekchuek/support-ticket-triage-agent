# Agent Tools

LangChain tools for the triage agent.

## Location

`src/modules/agents/tools/`

## Documentation

| Document | Description |
|----------|-------------|
| [kb_retrieval.md](kb_retrieval.md) | Knowledge base search tool |
| [customer_lookup.md](customer_lookup.md) | Customer information lookup tool |

## Overview

Tools extend the agent's capabilities by providing access to external systems:

- **KBRetrievalTool**: Search knowledge base for relevant articles using Qdrant
- **CustomerLookupTool**: Look up customer information from mock data

## Usage

```python
from src.modules.agents.tools.kb_retrieval import KBRetrievalTool
from src.modules.agents.tools.customer_lookup import CustomerLookupTool

# Initialize tools
kb_tool = KBRetrievalTool(collection_name="knowledge_base")
customer_tool = CustomerLookupTool(data_path="data/customers.json")

# Use with LangChain agent
tools = [kb_tool, customer_tool]
```

## See Also

- [BaseAgent](../base.md)
