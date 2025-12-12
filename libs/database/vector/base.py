"""Base abstraction for vector databases."""

from abc import ABC, abstractmethod
from typing import Any


class BaseVectorStore(ABC):
    """Abstract base class for vector databases.

    All vector store implementations must inherit from this class and implement
    all abstract methods. This enables swapping between different vector databases
    (FAISS, Pinecone, Weaviate, etc.) without changing application code.

    Note: Implementation-specific methods like count(), save(), load() are not
    included in the base class as they vary by vector DB type.
    """

    @abstractmethod
    def add(self, **kwargs) -> None:
        """Add embeddings to the store.

        Args:
            **kwargs: Implementation-specific parameters
                      (e.g., embeddings, metadata, ids)

        Raises:
            ValueError: If required parameters are missing or invalid
            Exception: If addition fails
        """
        pass

    @abstractmethod
    def search(self, **kwargs) -> list[dict[str, Any]]:
        """Search for similar embeddings.

        Args:
            **kwargs: Implementation-specific parameters
                      (e.g., query_embedding, k, filter)

        Returns:
            List of results, each containing:
            {
                "id": str,
                "score": float,
                "metadata": dict,
                "text": str (if available)
            }

        Raises:
            Exception: If search fails
        """
        pass

    @abstractmethod
    def delete(self, **kwargs) -> None:
        """Delete embeddings.

        Args:
            **kwargs: Implementation-specific deletion parameters
                      (e.g., ids, filter, conditions)

        Raises:
            Exception: If deletion fails
        """
        pass