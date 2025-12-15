# TechnicalAgent

Specialist agent for technical-related tickets.

## Location

`src/modules/agents/specialists/technical/main.py`

## Overview

Handles technical domain tickets including:
- System errors and outages (HTTP errors, downtime)
- Access and login issues
- Performance problems
- Bug reports
- Regional/infrastructure issues

## Class

```python
class TechnicalAgent(SpecialistBaseAgent):
    AGENT_NAME = "TechnicalAgent"
    PROMPT_ID = "triage_technical"
    DOMAIN = "technical"
```

## Inherits

- `SpecialistBaseAgent` - Shared specialist logic

## Tools

Uses shared `KBRetrievalTool` with `category_filter="technical"` for knowledge base search.

## Usage

```python
from src.modules.agents.specialists.technical.main import TechnicalAgent
from src.modules.agents.specialists.tools.kb_retrieval import KBRetrievalTool

kb_tool = KBRetrievalTool(vector_store=vs, llm=llm, category_filter="technical")
agent = TechnicalAgent(llm=llm, tools=[kb_tool], prompt_manager=pm)
```

## See Also

- [SpecialistBaseAgent](../base.md)
- [KBRetrievalTool](../tools/README.md)
