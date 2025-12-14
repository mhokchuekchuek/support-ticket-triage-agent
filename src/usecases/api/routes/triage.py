"""Triage route for processing support tickets."""
from fastapi import APIRouter, Request, HTTPException

from src.entities.ticket import Ticket
from src.entities.triage_result import TriageResult
from libs.logger.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(tags=["triage"])


@router.post("/triage", response_model=TriageResult)
async def triage_ticket(ticket: Ticket, request: Request) -> TriageResult:
    """Triage a support ticket.

    Args:
        ticket: Support ticket to triage.
        request: FastAPI request object.

    Returns:
        Triage result with urgency, action, and reasoning.

    Raises:
        HTTPException: If triage fails.
    """
    try:
        logger.info(f"Received triage request for ticket: {ticket.ticket_id}")

        workflow = request.app.state.triage_workflow
        result = workflow.invoke(ticket)

        if result.get("triage_result") is None:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate triage result",
            )

        logger.info(f"Triage complete for ticket: {ticket.ticket_id}")
        return result["triage_result"]

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Triage failed for ticket {ticket.ticket_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))
