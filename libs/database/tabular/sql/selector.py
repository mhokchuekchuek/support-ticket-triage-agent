"""SQL client selector for choosing provider implementation."""

from libs.base.selector import BaseToolSelector


class SQLClientSelector(BaseToolSelector):
    """Selector for SQL database providers.

    Available providers:
        - postgres: PostgreSQL database

    Example:
        >>> from libs.database.tabular.sql.selector import SQLClientSelector
        >>> client = SQLClientSelector.create(
        ...     provider="postgres",
        ...     host="postgres",
        ...     port=5432,
        ...     database="support_triage"
        ... )
    """

    _PROVIDERS = {
        "postgres": "libs.database.tabular.sql.postgres.main.PostgresSQLClient",
    }
