"""Redis client implementation."""

from typing import Any, Optional, List

import redis

from libs.database.keyvalue_db.base import BaseKeyValueClient
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class RedisClient(BaseKeyValueClient):
    """Redis key-value client implementation.

    Provides basic Redis CRUD operations.

    Attributes:
        client: Redis client instance.
    """

    def __init__(
        self,
        host: str = "redis",
        port: int = 6379,
        db: int = 0,
        decode_responses: bool = True,
        **kwargs
    ):
        """Initialize Redis client.

        Args:
            host: Redis host.
            port: Redis port.
            db: Redis database number.
            decode_responses: Decode byte responses to strings.
            **kwargs: Additional Redis connection parameters.
        """
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=decode_responses,
            **kwargs
        )
        logger.info(f"RedisClient connected to {host}:{port}")

    def get(self, key: str = None, **kwargs) -> Optional[Any]:
        """Get value by key.

        Args:
            key: Key to retrieve.

        Returns:
            Value if found, None otherwise.
        """
        if not key:
            raise ValueError("key is required")
        return self.client.get(key)

    def set(
        self,
        key: str = None,
        value: Any = None,
        ttl: Optional[int] = None,
        **kwargs
    ) -> bool:
        """Set key-value pair.

        Args:
            key: Key to set.
            value: Value to store.
            ttl: Time-to-live in seconds.

        Returns:
            True if successful.
        """
        if not key:
            raise ValueError("key is required")
        if ttl:
            return self.client.setex(key, ttl, value)
        return self.client.set(key, value)

    def delete(self, key: str = None, pattern: str = None, **kwargs) -> bool:
        """Delete key(s).

        Args:
            key: Single key to delete.
            pattern: Pattern to match and delete multiple keys.

        Returns:
            True if any keys were deleted.
        """
        if key:
            return self.client.delete(key) > 0
        if pattern:
            deleted = 0
            for k in self.client.scan_iter(pattern):
                self.client.delete(k)
                deleted += 1
            return deleted > 0
        raise ValueError("Either key or pattern is required")

    def scan(self, pattern: str = "*", **kwargs) -> List[str]:
        """Scan keys matching pattern.

        Args:
            pattern: Pattern to match (e.g., "session:*").

        Returns:
            List of matching keys.
        """
        return list(self.client.scan_iter(pattern))

    def get_raw_client(self) -> redis.Redis:
        """Get the underlying Redis client for direct operations.

        Returns:
            Redis client instance.
        """
        return self.client
