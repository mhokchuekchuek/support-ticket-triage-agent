"""FastAPI application factory."""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.usecases.api.routes import health, triage
from src.usecases.api.dependencies.triage import initialize_triage_workflow
from libs.configs.base import BaseConfigManager
from libs.logger.logger import get_logger

logger = get_logger(__name__)


def create_app(settings: BaseConfigManager) -> FastAPI:
    """Create and configure FastAPI application.

    Args:
        settings: Application settings (injected from main.py).

    Returns:
        Configured FastAPI application instance.
    """

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
        """Application lifespan manager."""
        logger.info("Starting up application...")
        app.state.triage_workflow = initialize_triage_workflow(settings)
        logger.info("Triage workflow initialized")
        yield
        logger.info("Shutting down application...")

    app = FastAPI(
        title="Support Ticket Triage API",
        description="AI-powered support ticket triage agent",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(triage.router, prefix="/api")

    return app
