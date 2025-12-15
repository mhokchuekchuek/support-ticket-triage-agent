# GeneralAgent

Specialist agent for general inquiries.

## Location

`src/modules/agents/specialists/general/main.py`

## Overview

Handles general domain tickets including:
- Feature questions and how-to guidance
- Account settings and preferences
- Product documentation and tutorials
- Feature requests and feedback

## Class

```python
class GeneralAgent(SpecialistBaseAgent):
    AGENT_NAME = "GeneralAgent"
    PROMPT_ID = "triage_general"
    DOMAIN = "general"
```

## Inherits

- `SpecialistBaseAgent` - Shared specialist logic

## Tools

Uses shared `KBRetrievalTool` with `category_filter="general"` for knowledge base search.

## Usage

```python
from src.modules.agents.specialists.general.main import GeneralAgent
from src.modules.agents.specialists.tools.kb_retrieval import KBRetrievalTool

kb_tool = KBRetrievalTool(vector_store=vs, llm=llm, category_filter="general")
agent = GeneralAgent(llm=llm, tools=[kb_tool], prompt_manager=pm)
```

## See Also

- [SpecialistBaseAgent](../base.md)
- [KBRetrievalTool](../tools/README.md)
