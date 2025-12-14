"""Prompt uploader for syncing local prompts to Langfuse.

Loads .prompt files with YAML frontmatter and uploads them to Langfuse.
"""

from pathlib import Path

import yaml

from libs.llm.prompt_manager.selector import PromptManagerSelector
from libs.logger.logger import get_logger
from libs.configs.base import BaseConfigManager
from libs.configs.selector import ConfigSelector

logger = get_logger(__name__)


class PromptUploader:
    """Uploads local .prompt files to Langfuse.

    Scans the prompts directory for .prompt files with YAML frontmatter,
    parses them, and uploads to Langfuse for centralized prompt management.

    Attributes:
        settings: Application settings from Dynaconf
        prompt_manager: Langfuse prompt manager client
        prompts_dir: Directory containing .prompt files
    """

    def __init__(self, settings: BaseConfigManager | None = None):
        """Initialize uploader with settings.

        Args:
            settings: Application settings. If None, creates new ConfigManager instance.
        """
        self.settings = settings or ConfigSelector.create(provider="dynaconf")

        # Initialize prompt manager
        self.prompt_manager = PromptManagerSelector.create(
            provider=self.settings.prompt_manager.langfuse.provider,
            public_key=self.settings.prompt_manager.langfuse.public_key,
            secret_key=self.settings.prompt_manager.langfuse.secret_key,
            host=self.settings.prompt_manager.langfuse.host,
        )

        # Get prompts configuration
        self.prompts_dir = Path(self.settings.prompts.directory)
        self.version = self.settings.prompts.version
        self.label = self.settings.prompts.label

        logger.info(
            f"PromptUploader initialized (dir={self.prompts_dir}, "
            f"version={self.version}, label={self.label})"
        )

    def load_prompts(self) -> list[dict]:
        """Load .prompt files from prompts directory.

        Scans the prompts directory for .prompt files and parses
        YAML frontmatter and template content.

        Returns:
            List of prompt dicts with name, config, template.

        Raises:
            FileNotFoundError: If prompts directory doesn't exist.
        """
        if not self.prompts_dir.exists():
            raise FileNotFoundError(f"Prompts directory not found: {self.prompts_dir}")

        prompts = []

        for prompt_file in self.prompts_dir.rglob("*.prompt"):
            try:
                parsed = self._parse_prompt_file(prompt_file)
                prompt_name = self._get_prompt_name(prompt_file)

                prompts.append({
                    "name": prompt_name,
                    "config": parsed["config"],
                    "template": parsed["template"],
                    "source_file": str(prompt_file),
                })
                logger.debug(f"Loaded prompt: {prompt_name}")
            except Exception as e:
                logger.warning(f"Failed to load {prompt_file}: {e}")
                continue

        logger.info(f"Loaded {len(prompts)} prompts from {self.prompts_dir}")
        return prompts

    def _parse_prompt_file(self, filepath: Path) -> dict:
        """Parse .prompt file with YAML frontmatter.

        Args:
            filepath: Path to .prompt file

        Returns:
            Dict with 'config' (frontmatter) and 'template' (content)
        """
        with open(filepath, "r") as f:
            content = f.read()

        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1].strip()
                template = parts[2].strip()
                config = yaml.safe_load(frontmatter) if frontmatter else {}
                return {"config": config, "template": template}

        return {"config": {}, "template": content.strip()}

    def _get_prompt_name(self, filepath: Path) -> str:
        """Generate prompt name from directory structure.

        prompts/triage/classifier/v1.prompt -> triage_classifier

        Args:
            filepath: Path to .prompt file

        Returns:
            Prompt name string
        """
        relative_path = filepath.relative_to(self.prompts_dir)
        parts = relative_path.parts

        if len(parts) >= 2:
            category = parts[0]
            name = parts[1]
            return f"{category}_{name}"

        return filepath.stem

    def process(self) -> int:
        """Upload all prompts to Langfuse.

        Loads prompts, validates them, and uploads to Langfuse.

        Returns:
            Number of successfully uploaded prompts.
        """
        if not self.prompt_manager.is_available():
            logger.error("Langfuse prompt manager is not available")
            return 0

        prompts = self.load_prompts()

        if not prompts:
            logger.warning("No prompts found to upload")
            return 0

        logger.info(f"Uploading {len(prompts)} prompts...")

        successful = 0
        for prompt in prompts:
            try:
                config = prompt["config"].copy()
                config["source_file"] = prompt["source_file"]
                config["version"] = self.version

                self.prompt_manager.upload_prompt(
                    name=prompt["name"],
                    prompt=prompt["template"],
                    config=config,
                    labels=[self.label, self.version],
                )

                successful += 1
                logger.info(f"Uploaded: {prompt['name']}")

            except Exception as e:
                logger.error(f"Failed to upload {prompt['name']}: {e}")
                continue

        logger.info(f"Successfully uploaded {successful}/{len(prompts)} prompts")
        return successful
