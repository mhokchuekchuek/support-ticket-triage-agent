"""Application settings using Dynaconf."""

from pathlib import Path

from dynaconf import Dynaconf


class Settings:
    """Application settings manager using Dynaconf."""

    def __init__(self) -> None:
        """Initialize settings from YAML, .env, and environment variables."""
        project_root = Path(__file__).resolve().parent.parent.parent
        configs_dir = project_root / "configs"

        # Get all YAML files (excluding litellm proxy config)
        config_files = sorted(configs_dir.glob("**/*.yaml"))
        settings_files = [
            str(f) for f in config_files if "proxy_config" not in f.name
        ]

        self._dynaconf = Dynaconf(
            settings_files=settings_files,
            envvar_prefix=False,
            environments=False,
            load_dotenv=True,
            dotenv_path=str(project_root / ".env"),
            nested_separator="__",
            merge_enabled=True,
        )

    def __getattr__(self, name: str):
        """Delegate attribute access to Dynaconf instance."""
        return getattr(self._dynaconf, name)
