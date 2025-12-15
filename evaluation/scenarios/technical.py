"""Technical ticket evaluation scenarios.

Tests the triage agent's ability to correctly classify and route
technical support tickets including critical outages and login issues.
"""

from src.entities.triage_result import UrgencyLevel, RecommendedAction

from evaluation.scenarios.base import (
    TriageScenario,
    WorkflowExpectation,
    TriageExpectation,
    CustomerProfile,
    TicketMessage,
    TicketCategory,
)


# Scenario 3: Critical System Outage - Enterprise
ENTERPRISE_OUTAGE = TriageScenario(
    id="technical-01-enterprise-outage",
    name="Enterprise System-Wide Outage",
    category=TicketCategory.TECHNICAL,
    description="Enterprise customer experiencing complete system outage - CRITICAL urgency requiring immediate escalation",
    messages=[
        TicketMessage(
            role="customer",
            content="URGENT: Our entire team of 45 people cannot access the platform. We're getting a 503 error on all endpoints. We have a critical client presentation in 2 hours and this is completely blocking our work!",
            timestamp="2024-11-15T08:00:00Z",
        )
    ],
    customer_profile=CustomerProfile(
        plan="enterprise",
        tenure_months=24,
        region="US",
        seats=45,
        previous_tickets=3,
    ),
    expected_workflow=WorkflowExpectation(
        agents_should_include=["translator", "supervisor"],
        agents_should_exclude=[],
        tools_should_include=["customer_lookup"],
        tools_should_exclude=[],
    ),
    expected_triage=TriageExpectation(
        expected_urgency=UrgencyLevel.CRITICAL,
        expected_action=RecommendedAction.ESCALATE_HUMAN,
        expected_ticket_type="technical",
        expected_sentiment="urgent",
        should_have_kb_articles=False,  # Escalation bypasses KB search
    ),
    expected_answer_criteria="""
Expected triage should:
1. Classify urgency as CRITICAL (enterprise + outage + time pressure)
2. Route for IMMEDIATE ESCALATION (requires_escalation=true)
3. Recommend ESCALATE_HUMAN (system-wide outage needs engineering)
4. Detect urgent sentiment (URGENT, "completely blocking")
5. Reasoning should cite: enterprise customer, 45 seats affected, time-critical deadline
6. Should trigger direct escalation path, not specialist agent
""",
)


# Scenario 4: Login Issue - High Urgency
LOGIN_FAILURE = TriageScenario(
    id="technical-02-login-failure",
    name="Repeated Login Failures",
    category=TicketCategory.TECHNICAL,
    description="Customer unable to login after multiple attempts - HIGH urgency requiring specialist investigation",
    messages=[
        TicketMessage(
            role="customer",
            content="I've been trying to log in for the past hour but keep getting 'Invalid credentials' error. I've reset my password 3 times and still can't get in. I need to access my account urgently for a deadline today.",
            timestamp="2024-11-15T11:30:00Z",
        )
    ],
    customer_profile=CustomerProfile(
        plan="pro",
        tenure_months=6,
        region="APAC",
        previous_tickets=2,
    ),
    expected_workflow=WorkflowExpectation(
        agents_should_include=["translator", "supervisor", "technical"],
        agents_should_exclude=["billing", "general"],
        tools_should_include=["customer_lookup", "kb_search"],
        tools_should_exclude=[],
    ),
    expected_triage=TriageExpectation(
        expected_urgency=UrgencyLevel.HIGH,
        expected_action=RecommendedAction.ROUTE_SPECIALIST,
        expected_ticket_type="technical",
        expected_sentiment="frustrated",
        should_have_kb_articles=True,
    ),
    expected_answer_criteria="""
Expected triage should:
1. Classify urgency as HIGH (blocking issue, multiple failed attempts, deadline)
2. Route to TECHNICAL specialist
3. Recommend ROUTE_SPECIALIST (needs account investigation)
4. Detect frustrated sentiment (repeated failures, urgent deadline)
5. Find KB articles about login troubleshooting, password reset
6. Reasoning should mention: repeated failures, time pressure, blocking issue
""",
)


# All technical scenarios
SCENARIOS = [ENTERPRISE_OUTAGE, LOGIN_FAILURE]
