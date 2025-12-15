# Tabular Database

Tabular/relational database implementations using the provider/selector pattern.

## Location

`libs/database/tabular/`

## Submodules

| Submodule | Purpose | Documentation |
|-----------|---------|---------------|
| SQL | SQL database clients | [sql/README.md](sql/README.md) |

## Architecture

```text
libs/database/tabular/
└── sql/              # SQL database clients
    ├── base.py       # BaseSQLClient abstract class
    ├── selector.py   # SQLClientSelector
    └── postgres/     # PostgreSQL client
```
