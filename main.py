"""Application entry point - injects configuration.

Run with: uvicorn main:app --reload
"""
from dotenv import load_dotenv

from libs.logger.logger import setup_logging, get_logger
from src.configs.settings import Settings
from src.usecases.api.app import create_app

# Load configuration at module level
load_dotenv()
settings = Settings()
setup_logging(level=settings.get("LOG_LEVEL", "INFO"))

logger = get_logger(__name__)
logger.info("Initializing application...")

# Create app instance for uvicorn
app = create_app(config=settings.as_dict())
