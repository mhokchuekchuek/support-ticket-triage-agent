from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class UrgencyLevel(str, Enum):
    """Urgency classification levels for support tickets."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RecommendedAction(str, Enum):
    """Recommended triage actions for support tickets."""

    AUTO_RESPOND = "auto_respond"
    ROUTE_SPECIALIST = "route_specialist"
    ESCALATE_HUMAN = "escalate_human"


class ExtractedInfo(BaseModel):
    """Information extracted from ticket analysis.

    Attributes:
        product_area: Product area affected by the issue.
        issue_type: Type of issue reported.
        sentiment: Customer sentiment (e.g., frustrated, neutral, positive).
        language: Detected language of the ticket.
    """

    product_area: Optional[str] = Field(None, description="Product area affected")
    issue_type: str = Field(..., description="Type of issue")
    sentiment: str = Field(..., description="Customer sentiment")
    language: str = Field(default="en", description="Detected language")


class RelevantArticle(BaseModel):
    """Knowledge base article reference.

    Attributes:
        id: Article unique identifier.
        title: Article title.
        relevance_score: How relevant this article is to the ticket (0-1).
    """

    id: str = Field(..., description="Article unique identifier")
    title: str = Field(..., description="Article title")
    relevance_score: float = Field(
        ..., ge=0, le=1, description="Relevance score between 0 and 1"
    )


class TriageResult(BaseModel):
    """Triage analysis output model.

    Contains the complete triage decision including urgency classification,
    extracted information, recommended action, and supporting context.

    Attributes:
        urgency: Urgency classification (critical/high/medium/low).
        extracted_info: Information extracted from ticket analysis.
        recommended_action: Recommended next action for this ticket.
        suggested_response: Optional AI-generated response suggestion.
        relevant_articles: List of relevant knowledge base articles.
        reasoning: Explanation for the triage decision.
    """

    urgency: UrgencyLevel = Field(..., description="Urgency classification")
    extracted_info: ExtractedInfo = Field(..., description="Extracted information")
    recommended_action: RecommendedAction = Field(
        ..., description="Recommended action"
    )
    suggested_response: Optional[str] = Field(
        None, description="Suggested response text"
    )
    relevant_articles: list[RelevantArticle] = Field(
        default_factory=list, description="Relevant knowledge base articles"
    )
    reasoning: str = Field(..., description="Explanation for the triage decision")
