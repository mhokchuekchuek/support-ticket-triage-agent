#!/usr/bin/env python3
"""Upload evaluation prompts to Langfuse.

Reads .prompt files from prompts/evaluation/ directory and uploads
them to Langfuse for use by the LLM-as-a-Judge evaluator.

Usage:
    python scripts/upload_evaluation_prompts.py

    # With custom label
    python scripts/upload_evaluation_prompts.py --label dev

Environment Variables:
    LANGFUSE_PUBLIC_KEY: Required for Langfuse authentication
    LANGFUSE_SECRET_KEY: Required for Langfuse authentication
    LANGFUSE_HOST: Langfuse host URL (default: https://cloud.langfuse.com)
"""

import argparse
import os
import sys
from pathlib import Path

import yaml

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from libs.logger.logger import get_logger, setup_logging

logger = get_logger(__name__)


def parse_prompt_file(file_path: Path) -> dict:
    """Parse a .prompt file with YAML frontmatter.

    Args:
        file_path: Path to the .prompt file

    Returns:
        Dictionary with 'metadata' and 'content' keys

    Raises:
        ValueError: If file format is invalid
    """
    content = file_path.read_text(encoding="utf-8")

    # Split frontmatter and content
    if not content.startswith("---"):
        raise ValueError(f"No YAML frontmatter found in {file_path}")

    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"Invalid frontmatter format in {file_path}")

    frontmatter = parts[1].strip()
    prompt_content = parts[2].strip()

    # Parse YAML frontmatter
    metadata = yaml.safe_load(frontmatter)

    return {
        "metadata": metadata,
        "content": prompt_content,
    }


def upload_prompts(
    prompts_dir: Path,
    label: str = "production",
) -> int:
    """Upload all evaluation prompts to Langfuse.

    Args:
        prompts_dir: Path to prompts/evaluation directory
        label: Label to assign to prompts (default: production)

    Returns:
        Number of prompts uploaded
    """
    from langfuse import Langfuse

    # Get Langfuse credentials from environment
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")
    host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

    if not public_key or not secret_key:
        raise ValueError(
            "LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY environment variables required"
        )

    # Initialize Langfuse client
    langfuse = Langfuse(
        public_key=public_key,
        secret_key=secret_key,
        host=host,
    )

    logger.info(f"Connected to Langfuse at {host}")

    # Find all .prompt files
    prompt_files = list(prompts_dir.glob("**/*.prompt"))
    logger.info(f"Found {len(prompt_files)} prompt files")

    uploaded = 0

    for prompt_file in prompt_files:
        try:
            # Parse the prompt file
            parsed = parse_prompt_file(prompt_file)
            metadata = parsed["metadata"]
            content = parsed["content"]

            # Get prompt name from metadata or generate from path
            prompt_name = metadata.get("name")
            if not prompt_name:
                # Generate name from directory structure
                # e.g., prompts/evaluation/triage_quality/v1.prompt -> evaluation_triage_quality
                rel_path = prompt_file.relative_to(prompts_dir)
                prompt_name = f"evaluation_{rel_path.parent.name}"

            # Upload to Langfuse
            logger.info(f"Uploading prompt: {prompt_name}")

            langfuse.create_prompt(
                name=prompt_name,
                prompt=content,
                config={
                    "model": metadata.get("model", "gpt-4"),
                    "temperature": metadata.get("temperature", 0.0),
                },
                labels=[label, metadata.get("category", "evaluation")],
            )

            logger.info(f"  Uploaded: {prompt_name} with label '{label}'")
            uploaded += 1

        except Exception as e:
            logger.error(f"Failed to upload {prompt_file}: {e}")

    # Flush to ensure all prompts are uploaded
    langfuse.flush()

    return uploaded


def main() -> int:
    """Main entry point for prompt upload.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    parser = argparse.ArgumentParser(
        description="Upload evaluation prompts to Langfuse"
    )
    parser.add_argument(
        "--label",
        type=str,
        default="production",
        help="Label to assign to prompts (default: production)",
    )
    parser.add_argument(
        "--prompts-dir",
        type=str,
        default=None,
        help="Path to prompts directory (default: prompts/evaluation)",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO)",
    )
    args = parser.parse_args()

    # Setup logging
    setup_logging(level=args.log_level)

    print("\n" + "=" * 60)
    print("Upload Evaluation Prompts to Langfuse")
    print("=" * 60 + "\n")

    try:
        # Determine prompts directory
        if args.prompts_dir:
            prompts_dir = Path(args.prompts_dir)
        else:
            prompts_dir = project_root / "prompts" / "evaluation"

        if not prompts_dir.exists():
            logger.error(f"Prompts directory not found: {prompts_dir}")
            return 1

        logger.info(f"Prompts directory: {prompts_dir}")
        logger.info(f"Label: {args.label}")

        # Upload prompts
        count = upload_prompts(prompts_dir, label=args.label)

        print(f"\nSuccessfully uploaded {count} prompts to Langfuse")
        print(f"Label: {args.label}")
        print("\n" + "=" * 60 + "\n")

        return 0

    except ValueError as e:
        logger.error(str(e))
        print(f"\nError: {e}")
        return 1

    except Exception as e:
        logger.error(f"Upload failed: {e}", exc_info=True)
        print(f"\nError: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
