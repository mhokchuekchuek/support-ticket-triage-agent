# Database Architecture

This document provides an overview of the database systems used in the Support Ticket Triage Agent.

## Overview

The system uses a **three-tier database architecture**:

| Database | Purpose | Port | Storage Type |
|----------|---------|------|--------------|
| **PostgreSQL** | Customer data, chat message history | 5432 | Relational |
| **Redis** | Session checkpointing, active workflows | 6379 | Key-Value |
| **Qdrant** | Knowledge base semantic search | 6333 | Vector |

## PostgreSQL Tables

### customers
Customer master data for the support system.
- [Full documentation](./customers.md)

### chat_messages
Conversation history for completed tickets.
- [Full documentation](./chat_messages.md)

## Schema Diagram

```
PostgreSQL Tables:
┌─────────────────────┐     ┌─────────────────────┐
│     customers       │     │   chat_messages     │
├─────────────────────┤     ├─────────────────────┤
│ id (PK)             │     │ ticket_id           │
│ name                │     │ customer_id         │
│ email               │     │ role                │
│ plan                │     │ content             │
│ tenure_months       │     │ created_at (PK)     │
│ region              │     └─────────────────────┘
│ seats               │
│ notes               │
│ created_at          │
└─────────────────────┘
```

## Connection Configuration

Environment variables for database connections:

```bash
# PostgreSQL
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=support_triage
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Qdrant
QDRANT_HOST=qdrant
QDRANT_PORT=6333
```

## Data Flow

See [Data Flow Documentation](./data_flow.md) for details on how data moves between databases.

## Related Files

| File | Purpose |
|------|---------|
| `scripts/init-db/02-create-tables.sql` | Table creation scripts |
| `libs/database/tabular/sql/postgres/main.py` | PostgreSQL client |
| `libs/database/keyvalue_db/redis/main.py` | Redis client |
| `libs/database/vector/qdrant/main.py` | Qdrant client |
