"""Application entry point - initializes config and injects to app.

Run with: uvicorn main:app --reload
"""
from dotenv import load_dotenv

from src.api.app import create_app
from libs.configs.selector import ConfigSelector
from libs.logger.logger import setup_logging, get_logger

load_dotenv()

settings = ConfigSelector.create(provider="dynaconf")
setup_logging(level=settings.get("LOG_LEVEL", "INFO"))

logger = get_logger(__name__)
logger.info("Initializing application...")

app = create_app(settings=settings)
