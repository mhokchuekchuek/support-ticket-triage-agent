"""Knowledge base processor for ingestion.

Loads markdown files with frontmatter and ingests them into Qdrant vector store.
"""

import uuid
from pathlib import Path

import frontmatter

from libs.database.vector.selector import VectorStoreSelector
from libs.llm.chunking.selector import TextChunkerSelector
from libs.llm.client.selector import LLMClientSelector
from libs.logger.logger import get_logger
from libs.configs.base import BaseConfigManager
from libs.configs.selector import ConfigSelector

logger = get_logger(__name__)


class KBProcessor:
    """Processes and ingests knowledge base articles into vector store.

    Loads markdown files with YAML frontmatter from the knowledge base directory,
    generates embeddings using LiteLLM proxy, and stores them in Qdrant.

    Attributes:
        settings: Application settings from Dynaconf
        vector_store: Qdrant vector store client
        llm_client: LiteLLM client for embeddings
        chunker: Text chunker for splitting documents
    """

    def __init__(self, settings: BaseConfigManager | None = None):
        """Initialize processor with settings.

        Args:
            settings: Application settings. If None, creates new ConfigManager instance.
        """
        self.settings = settings or ConfigSelector.create(provider="dynaconf")

        # Initialize vector store
        self.vector_store = VectorStoreSelector.create(
            provider=self.settings.ingestor.vectordb.provider,
            host=self.settings.ingestor.vectordb.host,
            port=self.settings.ingestor.vectordb.port,
            collection_name=self.settings.ingestor.vectordb.collection_name,
            vector_size=self.settings.ingestor.embedding.vector_size,
        )

        # Initialize LLM client for embeddings
        self.llm_client = LLMClientSelector.create(
            provider="litellm",
            proxy_url=self.settings.get("LITELLM_PROXY_URL", "http://localhost:4000"),
            embedding_model=self.settings.ingestor.embedding.model,
            api_key=self.settings.get("LITELLM_MASTER_KEY", "sk-1234"),
        )

        # Initialize text chunker
        self.chunker = TextChunkerSelector.create(
            provider="recursive",
            chunk_size=self.settings.ingestor.chunking.chunk_size,
            chunk_overlap=self.settings.ingestor.chunking.chunk_overlap,
        )

        logger.info(
            f"KBProcessor initialized (collection={self.settings.ingestor.vectordb.collection_name})"
        )

    def load_knowledge_base(self) -> list[dict]:
        """Load KB articles from markdown files with frontmatter.

        Scans the knowledge base directory for .md files and extracts
        frontmatter metadata and content.

        Returns:
            List of article dicts with id, title, content, category, keywords.

        Raises:
            FileNotFoundError: If knowledge base directory doesn't exist.
        """
        kb_dir = Path(self.settings.ingestor.kb_path)

        if not kb_dir.exists():
            raise FileNotFoundError(f"Knowledge base directory not found: {kb_dir}")

        articles = []

        for md_file in kb_dir.rglob("*.md"):
            try:
                post = frontmatter.load(md_file)
                article = {
                    "id": post.metadata.get("id"),
                    "title": post.metadata.get("title"),
                    "content": post.content,
                    "category": post.metadata.get("category"),
                    "keywords": post.metadata.get("keywords", []),
                }
                articles.append(article)
                logger.debug(f"Loaded article: {article['id']} - {article['title']}")
            except Exception as e:
                logger.warning(f"Failed to load {md_file}: {e}")
                continue

        logger.info(f"Loaded {len(articles)} articles from {kb_dir}")
        return articles

    def process(self) -> int:
        """Process and ingest all KB articles.

        Loads articles, chunks them, generates embeddings, and stores in vector database.

        Returns:
            Number of successfully ingested chunks.
        """
        articles = self.load_knowledge_base()

        if not articles:
            logger.warning("No articles found to ingest")
            return 0

        logger.info(f"Processing {len(articles)} articles...")

        # Prepare chunks for embedding
        all_chunks = []
        all_metadata = []
        all_ids = []

        for article in articles:
            # Combine title and content for better semantic search
            doc_text = f"{article['title']}\n\n{article['content']}"

            # Split document into chunks
            chunks = self.chunker.split(
                text=doc_text,
                metadata={
                    "article_id": article["id"],
                    "title": article["title"],
                    "category": article["category"],
                    "keywords": article.get("keywords", []),
                },
            )

            for chunk in chunks:
                all_chunks.append(chunk["text"])
                all_metadata.append({
                    **chunk["metadata"],
                    "text": chunk["text"],
                })
                # Generate UUID from article ID + chunk index (Qdrant requires UUID or int)
                chunk_id = f"{article['id']}_{chunk['metadata']['chunk_index']}"
                point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk_id))
                all_ids.append(point_id)

        logger.info(f"Split into {len(all_chunks)} chunks from {len(articles)} articles")

        # Generate embeddings via LiteLLM
        logger.info("Generating embeddings...")
        embeddings = self.llm_client.embed(all_chunks)

        # Add to vector store
        logger.info("Adding to vector store...")
        self.vector_store.add(
            embeddings=embeddings,
            metadata=all_metadata,
            ids=all_ids,
        )

        logger.info(f"Successfully ingested {len(all_chunks)} chunks")
        return len(all_chunks)
