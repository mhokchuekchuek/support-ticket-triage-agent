#!/usr/bin/env python
"""Script to ingest knowledge base into Qdrant vector store.

Usage:
    python scripts/ingest_kb.py

Environment Variables:
    OPENAI_API_KEY: Required for generating embeddings
    LOG_LEVEL: Logging level (default: INFO)
"""

import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from libs.logger.logger import get_logger, setup_logging
from libs.configs.selector import ConfigSelector
from ingestor.processor import KBProcessor


def main() -> int:
    """Main entry point for KB ingestion.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    # Initialize settings and logging
    settings = ConfigSelector.create(provider="dynaconf")
    setup_logging(level=settings.get("LOG_LEVEL", "INFO"))
    logger = get_logger(__name__)

    logger.info("Starting knowledge base ingestion...")

    try:
        processor = KBProcessor(settings=settings)
        count = processor.process()

        logger.info(f"Successfully ingested {count} articles into vector store")
        return 0

    except FileNotFoundError as e:
        logger.error(f"Knowledge base not found: {e}")
        return 1

    except Exception as e:
        logger.error(f"Ingestion failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
