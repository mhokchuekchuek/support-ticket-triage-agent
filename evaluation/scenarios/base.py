"""Base dataclasses for triage evaluation scenarios.

Defines the core data structures used to define test scenarios,
expected workflows, and triage outcomes for evaluation.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from src.entities.triage_result import UrgencyLevel, RecommendedAction


class TicketCategory(str, Enum):
    """Ticket category for scenario classification."""

    BILLING = "billing"
    TECHNICAL = "technical"
    GENERAL = "general"
    ESCALATION = "escalation"
    MULTILINGUAL = "multilingual"
    EDGE_CASE = "edge_case"


@dataclass
class WorkflowExpectation:
    """Expected workflow behavior for validation.

    Used to verify that the correct agents and tools were invoked
    during triage processing via Langfuse trace analysis.

    Attributes:
        agents_should_include: Agents that MUST be used (e.g., ["translator", "supervisor", "billing"])
        agents_should_exclude: Agents that should NOT be used
        tools_should_include: Tools that MUST be called (e.g., ["customer_lookup", "kb_search"])
        tools_should_exclude: Tools that should NOT be called
    """

    agents_should_include: List[str] = field(default_factory=list)
    agents_should_exclude: List[str] = field(default_factory=list)
    tools_should_include: List[str] = field(default_factory=list)
    tools_should_exclude: List[str] = field(default_factory=list)


@dataclass
class TriageExpectation:
    """Expected triage result for evaluation.

    Defines the expected outcome of triage for comparison against
    actual results during evaluation.

    Attributes:
        expected_urgency: Expected urgency level (critical/high/medium/low)
        expected_action: Expected recommended action
        expected_ticket_type: Expected routing (billing/technical/general)
        expected_language: Expected detected language code
        expected_sentiment: Expected sentiment classification
        should_have_kb_articles: Whether relevant KB articles should be returned
        min_kb_relevance_score: Minimum relevance score for KB articles
    """

    expected_urgency: UrgencyLevel
    expected_action: RecommendedAction
    expected_ticket_type: str
    expected_language: str = "en"
    expected_sentiment: Optional[str] = None
    should_have_kb_articles: bool = True
    min_kb_relevance_score: float = 0.5


@dataclass
class CustomerProfile:
    """Customer profile for test scenarios.

    Provides customer context that influences triage decisions
    such as plan type, tenure, and support history.

    Attributes:
        plan: Customer plan (free/pro/enterprise)
        tenure_months: Customer tenure in months
        region: Customer region (US/EU/APAC/LATAM)
        seats: Number of seats (for enterprise plans)
        previous_tickets: Number of previous support tickets
    """

    plan: str = "pro"
    tenure_months: int = 12
    region: str = "US"
    seats: Optional[int] = None
    previous_tickets: int = 2


@dataclass
class TicketMessage:
    """Single message in a test ticket.

    Represents a customer or agent message within a support ticket
    conversation.

    Attributes:
        role: Message sender (customer/agent)
        content: Message text content
        timestamp: ISO 8601 timestamp string
    """

    role: str
    content: str
    timestamp: str = "2024-11-15T10:30:00Z"


@dataclass
class TriageScenario:
    """Complete test scenario definition.

    Encapsulates all information needed to run and evaluate a single
    triage test case including input data and expected outcomes.

    Attributes:
        id: Unique scenario identifier (e.g., "billing-01-double-charge")
        name: Human-readable scenario name
        category: Scenario category for grouping and filtering
        description: Detailed description of what this scenario tests
        messages: List of ticket messages to process
        customer_profile: Customer context for the ticket
        expected_workflow: Expected agent/tool workflow
        expected_triage: Expected triage result
        expected_answer_criteria: Detailed criteria for LLM judge evaluation
    """

    id: str
    name: str
    category: TicketCategory
    description: str
    messages: List[TicketMessage]
    customer_profile: CustomerProfile
    expected_workflow: WorkflowExpectation
    expected_triage: TriageExpectation
    expected_answer_criteria: str = ""
