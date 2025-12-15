"""Health check route."""
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict:
    """Health check endpoint.

    Returns:
        Health status dict.
    """
    return {"status": "healthy"}
