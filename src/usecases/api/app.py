"""FastAPI application factory."""
from fastapi import FastAPI


def create_app(config: dict) -> FastAPI:
    """Create FastAPI application.

    Args:
        config: Application configuration dict (injected from main.py)
    """
    app = FastAPI(
        title=config.get("APP_TITLE", "Support Ticket Triage Agent"),
        version=config.get("APP_VERSION", "0.1.0"),
    )

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    return app
