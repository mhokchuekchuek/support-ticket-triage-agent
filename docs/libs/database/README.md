# Database Module

Database utilities and integrations.

## Location

`libs/database/`

## Submodules

| Submodule | Purpose | Documentation |
|-----------|---------|---------------|
| Vector | Vector database clients | [vector/README.md](vector/README.md) |

## Architecture

```text
libs/database/
└── vector/           # Vector database clients
    ├── base.py       # BaseVectorStore abstract class
    ├── selector.py   # VectorStoreSelector
    └── qdrant/       # Qdrant client
```
