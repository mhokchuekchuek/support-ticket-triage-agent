"""Vector store selector for choosing provider implementation."""

from libs.base.selector import BaseToolSelector


class VectorStoreSelector(BaseToolSelector):
    """Selector for vector store providers.

    Available providers:
        - qdrant: Qdrant vector database

    Example:
        >>> from libs.database.vector.selector import VectorStoreSelector
        >>> store = VectorStoreSelector.create(
        ...     provider="qdrant",
        ...     host="qdrant",
        ...     port=6333,
        ...     collection_name="documents"
        ... )
    """

    _PROVIDERS = {
        "qdrant": "libs.database.vector.qdrant.main.VectorStoreClient",
    }
