"""Knowledge base retrieval tool for searching documentation."""

from langchain.tools import BaseTool
from pydantic import Field, BaseModel
from typing import Type, Any, Optional

from libs.database.vector.base import BaseVectorStore
from libs.llm.client.base import BaseLLM
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class KBRetrievalInput(BaseModel):
    """Input schema for KB retrieval tool."""

    query: str = Field(description="Search query for knowledge base")
    top_k: int = Field(default=3, description="Number of results to return")


class KBRetrievalTool(BaseTool):
    """Search the knowledge base for relevant articles.

    Use this tool to find documentation, FAQs, and troubleshooting guides
    related to customer issues.

    Supports optional category filtering to search domain-specific content
    (billing, technical, general).

    Attributes:
        name: Tool name for LangChain.
        description: Tool description for the LLM.
        vector_store: Vector store client for search (injected).
        llm: LLM client for query embedding (injected).
        category_filter: Optional category to filter results by.
    """

    name: str = "kb_search"
    description: str = (
        "Search the knowledge base for relevant articles. "
        "Use this to find documentation, FAQs, and troubleshooting guides "
        "related to customer issues."
    )
    args_schema: Type[BaseModel] = KBRetrievalInput
    vector_store: Any = None
    llm: Any = None
    category_filter: Optional[str] = None

    def __init__(
        self,
        vector_store: BaseVectorStore,
        llm: BaseLLM,
        category_filter: Optional[str] = None,
        **kwargs,
    ):
        """Initialize KB retrieval tool.

        Args:
            vector_store: Vector store client for KB search.
            llm: LLM client with embedding capability.
            category_filter: Optional category to filter by (billing, technical, general).
            **kwargs: Additional arguments passed to BaseTool.
        """
        super().__init__(**kwargs)
        self.vector_store = vector_store
        self.llm = llm
        self.category_filter = category_filter

        if category_filter:
            logger.info(f"KBRetrievalTool initialized with category filter: {category_filter}")
        else:
            logger.info("KBRetrievalTool initialized (no category filter)")

    def _run(self, query: str, top_k: int = 3) -> str:
        """Execute KB search.

        Args:
            query: Search query string.
            top_k: Number of results to return.

        Returns:
            Formatted string with relevant KB articles.
        """
        logger.info(f"Searching KB for: {query}")
        if self.category_filter:
            logger.info(f"Filtering by category: {self.category_filter}")

        # Generate query embedding
        query_embedding = self.llm.embed([query])[0]

        # Build filter if category is specified
        search_filter = None
        if self.category_filter:
            search_filter = {"category": self.category_filter}

        # Search vector store
        results = self.vector_store.search(
            query_embedding=query_embedding,
            k=top_k,
            filter=search_filter,
        )

        if not results:
            return "No relevant articles found."

        # Format results
        formatted = []
        for r in results:
            text = r.get("text", r.get("metadata", {}).get("text", ""))
            title = r.get("metadata", {}).get("title", "Untitled")
            article_id = r.get("metadata", {}).get("article_id", "unknown")
            category = r.get("metadata", {}).get("category", "general")

            formatted.append(
                f"**{title}** (id: {article_id}, category: {category}, relevance: {r['score']:.2f})\n"
                f"{text[:500]}..."
            )

        return "\n\n---\n\n".join(formatted)
