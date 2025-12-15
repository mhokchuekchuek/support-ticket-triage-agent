# Entities

Domain data models for the support ticket triage system.

## Location

`src/entities/`

## Documentation

| Document | Description |
|----------|-------------|
| [ticket.md](ticket.md) | Ticket, TicketMessage, CustomerInfo models |
| [triage_result.md](triage_result.md) | TriageResult, UrgencyLevel, RecommendedAction, ExtractedInfo, RelevantArticle models |
| [answer.md](answer.md) | AnswerRequest, AnswerResponse models |
| [sql_records.md](sql_records.md) | CustomerRecord, TicketRecord, ChatMessage models |

## Overview

Entities are Pydantic models that define the core data structures:

- **Input Models**: `Ticket`, `TicketMessage`, `CustomerInfo` - represent incoming support tickets
- **Output Models**: `TriageResult`, `ExtractedInfo`, `RelevantArticle` - represent triage analysis results
- **Answer Models**: `AnswerRequest`, `AnswerResponse` - client chat message storage
- **SQL Record Models**: `CustomerRecord`, `TicketRecord`, `ChatMessage` - database storage entities
- **Enums**: `UrgencyLevel`, `RecommendedAction` - classification constants

## Usage

```python
from src.entities.ticket import Ticket, TicketMessage, CustomerInfo
from src.entities.triage_result import TriageResult, UrgencyLevel, RecommendedAction
from src.entities.customer_record import CustomerRecord
from src.entities.ticket_record import TicketRecord
from src.entities.chat_message import ChatMessage
```

## See Also

- [Architecture](../../architecture/README.md)
