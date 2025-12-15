# Specialist Agent Tools

LangChain tools for the specialist triage agents.

## Location

Specialist tools are in `src/modules/agents/specialists/tools/`. Other agent-specific tools are in their respective agent folders.

## Tool Locations

| Tool | Location | Used By |
|------|----------|---------|
| `KBRetrievalTool` | `src/modules/agents/specialists/tools/kb_retrieval.py` | BillingAgent, TechnicalAgent, GeneralAgent |
| `CustomerLookupTool` | `src/modules/agents/supervisor/tools/customer_lookup.py` | SupervisorAgent |
| `TicketSummarizeTool` | `src/modules/agents/ticket_matcher/tools/ticket_summarize.py` | TicketMatcherAgent |

## Specialist Tools

### KBRetrievalTool

Search knowledge base for relevant articles using Qdrant vector store.

**Location**: `src/modules/agents/specialists/tools/kb_retrieval.py`

Used by specialist agents (billing, technical, general) with different category filters.

```python
from src.modules.agents.specialists.tools.kb_retrieval import KBRetrievalTool

kb_tool = KBRetrievalTool(
    vector_store=vector_store,
    llm=embedding_client,
    category_filter="billing",  # or "technical", "general"
)
```

## Other Agent Tools

### SupervisorAgent Tools

Located in `src/modules/agents/supervisor/tools/`:

- **CustomerLookupTool**: Look up customer information from PostgreSQL `customers` table

```python
from src.modules.agents.supervisor.tools.customer_lookup import CustomerLookupTool

customer_tool = CustomerLookupTool(db_client=sql_client)
```

### TicketMatcherAgent Tools

Located in `src/modules/agents/ticket_matcher/tools/`:

- **TicketSummarizeTool**: Summarize active ticket from Redis checkpoint

```python
from src.modules.agents.ticket_matcher.tools.ticket_summarize import TicketSummarizeTool
```

## See Also

- [Agents](../../README.md)
- [Specialists](../README.md)
- [SupervisorAgent](../../supervisor/README.md)
- [TicketMatcherAgent](../../ticket_matcher/README.md)
- [Database Documentation](/docs/db/README.md)
