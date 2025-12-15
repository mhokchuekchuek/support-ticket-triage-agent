# Modules

Core modules for the ticket triage system.

## Components

| Module | Description | Docs |
|--------|-------------|------|
| `agents/` | Multi-agent system (translator, supervisor, specialists) | [agents/README.md](agents/README.md) |
| `graph/` | LangGraph workflow orchestration | [graph/README.md](graph/README.md) |

## Architecture

```
modules/
├── agents/
│   ├── translator/     # Language detection & translation
│   ├── supervisor/     # Classification & routing
│   ├── specialists/    # Billing, Technical, General agents
│   └── ticket_matcher/ # Match messages to existing tickets
└── graph/
    └── workflow.py     # LangGraph multi-agent workflow
```
