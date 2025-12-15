"""Configuration loader for evaluation pipeline.

Uses libs/configs for consistent configuration management across the project.
"""

from libs.configs.selector import ConfigSelector
from libs.configs.base import BaseConfigManager
from libs.logger.logger import get_logger

logger = get_logger(__name__)


def get_evaluation_config() -> BaseConfigManager:
    """Get evaluation configuration using libs/configs.

    Uses the shared ConfigSelector to load configuration from
    configs/evaluation.yaml with environment variable overrides.

    Returns:
        ConfigManager instance with evaluation settings

    Example:
        >>> config = get_evaluation_config()
        >>> print(config.evaluation.api_url)
        'http://localhost:8000'
        >>> print(config.evaluation.llm.model)
        'gpt-4'
    """
    settings = ConfigSelector.create(provider="dynaconf")
    logger.info("Loaded evaluation config via libs/configs")
    return settings
