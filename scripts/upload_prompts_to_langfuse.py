#!/usr/bin/env python
"""Script to upload prompts to Langfuse.

Usage:
    python scripts/upload_prompts_to_langfuse.py

Environment Variables:
    LANGFUSE_PUBLIC_KEY: Required for Langfuse authentication
    LANGFUSE_SECRET_KEY: Required for Langfuse authentication
    LOG_LEVEL: Logging level (default: INFO)
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from libs.logger.logger import get_logger, setup_logging
from libs.configs.selector import ConfigSelector
from prompts.uploader import PromptUploader


def main() -> int:
    """Main entry point for prompt upload.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    settings = ConfigSelector.create(provider="dynaconf")
    setup_logging(level=settings.get("LOG_LEVEL", "INFO"))
    logger = get_logger(__name__)

    logger.info("Starting prompt upload to Langfuse...")

    try:
        uploader = PromptUploader(settings=settings)
        count = uploader.process()

        logger.info(f"Successfully uploaded {count} prompts to Langfuse")
        return 0

    except FileNotFoundError as e:
        logger.error(f"Prompts directory not found: {e}")
        return 1

    except Exception as e:
        logger.error(f"Upload failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
