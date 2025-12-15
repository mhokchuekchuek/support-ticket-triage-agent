# Key-Value Database

Abstraction layer for key-value databases.

## Location

`libs/database/keyvalue_db/`

## Documentation

| Document | Description |
|----------|-------------|
| [redis.md](redis.md) | Redis client implementation |

## Overview

The keyvalue_db module provides a provider-agnostic interface for key-value stores:

- **BaseKeyValueClient**: Abstract base class defining the interface
- **KeyValueClientSelector**: Factory for creating provider instances
- **RedisClient**: Redis implementation

## Usage

```python
from libs.database.keyvalue_db.selector import KeyValueClientSelector

# Create Redis client
client = KeyValueClientSelector.create(
    provider="redis",
    host="redis",
    port=6379
)

# Basic operations
client.set(key="session:123", value="data")
value = client.get(key="session:123")
client.delete(key="session:123")

# Scan keys by pattern
keys = client.scan(pattern="session:*")
```

## Providers

| Provider | Description |
|----------|-------------|
| `redis` | Redis key-value store |

## See Also

- [SQL Database](../tabular/README.md)
- [Vector Database](../vector/README.md)
