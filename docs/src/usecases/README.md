# Use Cases Layer

Application-specific business logic orchestration.

## Overview

The Use Cases layer contains application business rules that orchestrate domain entities and coordinate with repositories for data persistence.

## Structure

```
src/usecases/
└── triage/
    └── main.py             # TriageService
```

## Layer Rules

| DO | DO NOT |
|----|--------|
| Orchestrate domain logic | Contain SQL/Redis code |
| Use repositories for data access | Format API responses |
| Implement application workflows | Import from outer layers |
| Coordinate between modules | Access infrastructure directly |

## Services

| Service | Location | Description |
|---------|----------|-------------|
| [TriageService](triage/README.md) | `triage/main.py` | Ticket triage workflow orchestration |

## Dependencies

```
Use Cases (Services)
    ↓
Entities, Modules (agents, graph)
    ↓
Repositories
    ↓
Infrastructure (libs/database)
```

## Terminology

| Term | Storage | Description |
|------|---------|-------------|
| Activated ticket | Redis | In-progress, waiting for follow-up |
| Completed ticket | PostgreSQL | Resolved or escalated, closed |
