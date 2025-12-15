# Redis Client

Redis key-value client implementation.

## Location

`libs/database/keyvalue_db/redis/main.py`

## Configuration

Accepts all parameters from [redis-py](https://redis-py.readthedocs.io/en/stable/connections.html#redis.Redis):

```python
client = KeyValueClientSelector.create(
    provider="redis",
    host="redis",
    port=6379,
    db=0,
    decode_responses=True,
    # ... any other redis.Redis parameters
)
```

## Methods

All methods follow the `**kwargs` pattern defined in `BaseKeyValueClient`.

### get

```python
value = client.get(key="session:123")
```

### set

```python
client.set(key="session:123", value="data", ttl=60)
```

### delete

```python
client.delete(key="session:123")
client.delete(pattern="session:*")
```

### scan

```python
keys = client.scan(pattern="session:*")
```

### get_raw_client

Returns underlying `redis.Redis` for advanced operations.

```python
raw = client.get_raw_client()
```

## Reference

- [redis-py Documentation](https://redis-py.readthedocs.io/)

## See Also

- [BaseKeyValueClient](README.md)
