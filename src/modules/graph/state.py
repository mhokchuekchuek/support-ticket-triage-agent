"""State definitions for multi-agent triage workflow."""

from enum import Enum
from typing import Annotated, Optional, TypedDict, Literal

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

from src.entities.ticket import Ticket
from src.entities.triage_result import TriageResult, UrgencyLevel


class TicketType(str, Enum):
    """Classification of ticket types for routing."""

    BILLING = "billing"
    TECHNICAL = "technical"
    GENERAL = "general"


class TranslationResult(BaseModel):
    """Result from translator agent.

    Attributes:
        original_language: Detected language code (e.g., 'th', 'en', 'es').
        is_english: Whether the ticket is in English.
        translated_messages: Translated message contents (if non-English).
        original_messages: Original message contents preserved for response.
    """

    original_language: str = Field(..., description="Detected language code")
    is_english: bool = Field(..., description="Whether ticket is in English")
    translated_messages: Optional[list[str]] = Field(
        None, description="Translated messages if non-English"
    )
    original_messages: list[str] = Field(
        ..., description="Original messages preserved"
    )


class SupervisorDecision(BaseModel):
    """Supervisor's routing decision.

    Attributes:
        urgency: Classified urgency level.
        ticket_type: Detected ticket type for routing.
        reasoning: Brief explanation for the classification.
        requires_escalation: Whether to skip specialist and escalate directly.
    """

    urgency: UrgencyLevel = Field(..., description="Urgency classification")
    ticket_type: TicketType = Field(..., description="Ticket type for routing")
    reasoning: str = Field(..., description="Classification reasoning")
    requires_escalation: bool = Field(
        default=False, description="Skip specialist, escalate directly"
    )


class AgentState(TypedDict):
    """State passed between nodes in the multi-agent triage workflow.

    This state is shared across all agents in the workflow:
    - TranslatorAgent: Detects language and translates if needed
    - SupervisorAgent: Classifies and routes to specialists
    - Specialist Agents: Handle domain-specific triage (billing/technical/general)

    Attributes:
        messages: Message history with automatic accumulation.
        ticket: Input ticket being processed.
        customer_info: Customer information from lookup.
        translation: Translation result if ticket was non-English.
        supervisor_decision: Supervisor's classification and routing decision.
        kb_results: Knowledge base search results from specialist.
        triage_result: Final triage result.
        iteration: Iteration counter for loop control.
        current_agent: Name of the currently executing agent.
    """

    messages: Annotated[list[BaseMessage], add_messages]
    ticket: Ticket
    customer_info: Optional[dict]
    translation: Optional[TranslationResult]
    supervisor_decision: Optional[SupervisorDecision]
    kb_results: Optional[list[dict]]
    triage_result: Optional[TriageResult]
    iteration: int
    current_agent: Optional[str]


def create_initial_state(ticket: Ticket) -> AgentState:
    """Create initial state from a ticket.

    Args:
        ticket: Support ticket to process.

    Returns:
        Initial AgentState with the ticket set.
    """
    return AgentState(
        messages=[],
        ticket=ticket,
        customer_info=None,
        translation=None,
        supervisor_decision=None,
        kb_results=None,
        triage_result=None,
        iteration=0,
        current_agent=None,
    )
