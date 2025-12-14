"""Dynaconf-based configuration manager implementation."""

from pathlib import Path
from typing import Any

from dynaconf import Dynaconf

from libs.configs.base import BaseConfigManager
from libs.logger.logger import get_logger

logger = get_logger(__name__)


class ConfigManager(BaseConfigManager):
    """Configuration manager using Dynaconf.

    Loads configuration from YAML files, .env files, and environment variables.
    Supports nested configuration access via dot notation and attribute access.

    Attributes:
        project_root: Path to the project root directory
        configs_dir: Path to the configuration directory
    """

    def __init__(
        self,
        project_root: str | Path | None = None,
        configs_dir: str | Path = "configs",
        env_file: str | Path = ".env",
        exclude_patterns: list[str] | None = None,
        envvar_prefix: str | bool = False,
        environments: bool = False,
        nested_separator: str = "__",
        merge_enabled: bool = True,
    ) -> None:
        """Initialize configuration manager.

        Args:
            project_root: Path to project root. If None, auto-detects by looking
                for markers like .git, pyproject.toml, setup.py
            configs_dir: Directory name or path containing YAML config files.
                If relative, resolved against project_root
            env_file: Name or path to .env file. If relative, resolved against project_root
            exclude_patterns: List of filename patterns to exclude (e.g., ["proxy_config"])
            envvar_prefix: Prefix for environment variables (False = no prefix)
            environments: Enable Dynaconf environments (development, production, etc.)
            nested_separator: Separator for nested env vars (e.g., DB__HOST)
            merge_enabled: Enable merging of nested config dicts
        """
        self.project_root = self._resolve_project_root(project_root)
        self.configs_dir = self._resolve_configs_dir(configs_dir)
        self._exclude_patterns = exclude_patterns or ["proxy_config"]

        # Build settings files list
        settings_files = self._get_settings_files()

        # Resolve env file path
        env_path = self._resolve_path(env_file)

        self._dynaconf = Dynaconf(
            settings_files=settings_files,
            envvar_prefix=envvar_prefix,
            environments=environments,
            load_dotenv=True,
            dotenv_path=str(env_path) if env_path.exists() else None,
            nested_separator=nested_separator,
            merge_enabled=merge_enabled,
        )

        logger.info(
            f"ConfigManager initialized (root={self.project_root}, "
            f"configs={self.configs_dir}, files={len(settings_files)})"
        )

    def _resolve_project_root(self, project_root: str | Path | None) -> Path:
        """Resolve project root directory.

        Args:
            project_root: Explicit project root or None for auto-detection

        Returns:
            Resolved project root path
        """
        if project_root is not None:
            return Path(project_root).resolve()

        # Auto-detect by looking for common project markers
        markers = [".git", "pyproject.toml", "setup.py", "setup.cfg", "requirements.txt"]
        current = Path.cwd()

        for parent in [current, *current.parents]:
            for marker in markers:
                if (parent / marker).exists():
                    return parent

        # Fallback to current working directory
        logger.warning("Could not auto-detect project root, using cwd")
        return current

    def _resolve_configs_dir(self, configs_dir: str | Path) -> Path:
        """Resolve configuration directory path.

        Args:
            configs_dir: Directory name or absolute path

        Returns:
            Resolved configs directory path
        """
        configs_path = Path(configs_dir)
        if configs_path.is_absolute():
            return configs_path
        return self.project_root / configs_path

    def _resolve_path(self, path: str | Path) -> Path:
        """Resolve a path relative to project root.

        Args:
            path: Absolute or relative path

        Returns:
            Resolved absolute path
        """
        path = Path(path)
        if path.is_absolute():
            return path
        return self.project_root / path

    def _get_settings_files(self) -> list[str]:
        """Get list of settings files to load.

        Returns:
            List of absolute paths to YAML config files
        """
        if not self.configs_dir.exists():
            logger.warning(f"Configs directory not found: {self.configs_dir}")
            return []

        config_files = sorted(self.configs_dir.glob("**/*.yaml"))
        settings_files = []

        for f in config_files:
            # Check if file matches any exclude pattern
            excluded = any(
                pattern in f.name for pattern in self._exclude_patterns
            )
            if not excluded:
                settings_files.append(str(f))

        return settings_files

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key.

        Args:
            key: Configuration key (supports nested keys with dot notation)
            default: Default value if key is not found

        Returns:
            Configuration value or default
        """
        return self._dynaconf.get(key, default)

    def as_dict(self) -> dict[str, Any]:
        """Get all configuration as a dictionary.

        Returns:
            Dictionary containing all configuration values
        """
        return self._dynaconf.as_dict()

    def __getattr__(self, name: str) -> Any:
        """Delegate attribute access to Dynaconf instance.

        Args:
            name: Configuration key

        Returns:
            Configuration value
        """
        # Avoid infinite recursion for internal attributes
        if name.startswith("_"):
            raise AttributeError(f"'{type(self).__name__}' has no attribute '{name}'")
        return getattr(self._dynaconf, name)
