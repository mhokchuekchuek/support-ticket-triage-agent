"""Key-value client selector for choosing provider implementation."""

from libs.base.selector import BaseToolSelector


class KeyValueClientSelector(BaseToolSelector):
    """Selector for key-value store providers.

    Available providers:
        - redis: Redis key-value store

    Example:
        >>> from libs.database.keyvalue_db.selector import KeyValueClientSelector
        >>> client = KeyValueClientSelector.create(
        ...     provider="redis",
        ...     host="redis",
        ...     port=6379
        ... )
    """

    _PROVIDERS = {
        "redis": "libs.database.keyvalue_db.redis.main.RedisClient",
    }
