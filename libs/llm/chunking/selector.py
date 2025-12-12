"""Text chunker selector for choosing provider implementation."""

from libs.base.selector import BaseToolSelector


class TextChunkerSelector(BaseToolSelector):
    """Selector for text chunker providers.

    Available providers:
        - recursive: Recursive character text splitter

    Example:
        >>> from libs.llm.chunking.selector import TextChunkerSelector
        >>> chunker = TextChunkerSelector.create(
        ...     provider="recursive",
        ...     chunk_size=1000,
        ...     chunk_overlap=200
        ... )
    """

    _PROVIDERS = {
        "recursive": "libs.llm.chunking.recursive.main.TextChunker",
    }
