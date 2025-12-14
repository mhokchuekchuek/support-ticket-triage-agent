"""Configuration manager selector for choosing provider implementation."""

from libs.base.selector import BaseToolSelector


class ConfigSelector(BaseToolSelector):
    """Selector for configuration manager providers.

    Available providers:
        - dynaconf: Dynaconf-based configuration manager

    Example:
        >>> from libs.configs.selector import ConfigSelector
        >>>
        >>> # With explicit project root
        >>> settings = ConfigSelector.create(
        ...     provider="dynaconf",
        ...     project_root="/path/to/project",
        ...     configs_dir="configs",
        ...     env_file=".env"
        ... )
        >>>
        >>> # Auto-detect project root (looks for .git, pyproject.toml, etc.)
        >>> settings = ConfigSelector.create(provider="dynaconf")
        >>>
        >>> # Access configuration
        >>> log_level = settings.get("LOG_LEVEL", "INFO")
        >>> db_config = settings.database
    """

    _PROVIDERS = {
        "dynaconf": "libs.configs.dynaconf.main.ConfigManager",
    }
