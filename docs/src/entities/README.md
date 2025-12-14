# Entities

Domain data models for the support ticket triage system.

## Location

`src/entities/`

## Documentation

| Document | Description |
|----------|-------------|
| [ticket.md](ticket.md) | Ticket, TicketMessage, CustomerInfo models |
| [triage_result.md](triage_result.md) | TriageResult, UrgencyLevel, RecommendedAction, ExtractedInfo, RelevantArticle models |

## Overview

Entities are Pydantic models that define the core data structures:

- **Input Models**: `Ticket`, `TicketMessage`, `CustomerInfo` - represent incoming support tickets
- **Output Models**: `TriageResult`, `ExtractedInfo`, `RelevantArticle` - represent triage analysis results
- **Enums**: `UrgencyLevel`, `RecommendedAction` - classification constants

## Usage

```python
from src.entities.ticket import Ticket, TicketMessage, CustomerInfo
from src.entities.triage_result import TriageResult, UrgencyLevel, RecommendedAction
```

## See Also

- [Architecture](../../architecture/README.md)
