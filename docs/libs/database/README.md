# Database Module

Database utilities and integrations.

## Location

`libs/database/`

## Database Schema Documentation

For detailed database schema, tables, and data flow documentation, see:

**[/docs/db/](../../db/README.md)** - Complete database architecture documentation

## Submodules

| Submodule | Purpose | Documentation |
|-----------|---------|---------------|
| Vector | Vector database clients | [vector/README.md](vector/README.md) |
| Tabular | Tabular/relational database clients | [tabular/README.md](tabular/README.md) |
| Key-Value | Key-value store clients | [keyvalue_db/README.md](keyvalue_db/README.md) |

## Architecture

```text
libs/database/
├── vector/           # Vector database clients
│   ├── base.py       # BaseVectorStore abstract class
│   ├── selector.py   # VectorStoreSelector
│   └── qdrant/       # Qdrant client
├── tabular/          # Tabular/relational database clients
│   └── sql/          # SQL database clients
│       ├── base.py       # BaseSQLClient abstract class
│       ├── selector.py   # SQLClientSelector
│       └── postgres/     # PostgreSQL client
└── keyvalue_db/      # Key-value store clients
    ├── base.py       # BaseKeyValueClient abstract class
    ├── selector.py   # KeyValueClientSelector
    └── redis/        # Redis client
```

## PostgreSQL Tables

| Table | Purpose | Documentation |
|-------|---------|---------------|
| `customers` | Customer master data | [/docs/db/customers.md](../../db/customers.md) |
| `chat_messages` | Conversation history | [/docs/db/chat_messages.md](../../db/chat_messages.md) |
