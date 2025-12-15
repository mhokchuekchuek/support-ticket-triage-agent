# BillingAgent

Specialist agent for billing-related tickets.

## Location

`src/modules/agents/specialists/billing/main.py`

## Overview

Handles billing domain tickets including:
- Payment failures and processing issues
- Refund requests and charge disputes
- Subscription changes (upgrades, downgrades, cancellations)
- Invoice and billing inquiries

## Class

```python
class BillingAgent(SpecialistBaseAgent):
    AGENT_NAME = "BillingAgent"
    PROMPT_ID = "triage_billing"
    DOMAIN = "billing"
```

## Inherits

- `SpecialistBaseAgent` - Shared specialist logic

## Tools

Uses shared `KBRetrievalTool` with `category_filter="billing"` for knowledge base search.

## Usage

```python
from src.modules.agents.specialists.billing.main import BillingAgent
from src.modules.agents.specialists.tools.kb_retrieval import KBRetrievalTool

kb_tool = KBRetrievalTool(vector_store=vs, llm=llm, category_filter="billing")
agent = BillingAgent(llm=llm, tools=[kb_tool], prompt_manager=pm)
```

## See Also

- [SpecialistBaseAgent](../base.md)
- [KBRetrievalTool](../tools/README.md)
