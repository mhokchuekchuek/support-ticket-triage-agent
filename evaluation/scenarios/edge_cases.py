"""Edge case and ambiguous query scenarios.

Tests the triage agent's handling of ambiguous, incomplete, or
complex tickets that don't fit cleanly into standard categories.
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


# Scenario 10: Ambiguous Query
AMBIGUOUS_QUERY = TriageScenario(
    id="edge-01-ambiguous",
    name="Ambiguous Query - Missing Context",
    category=TicketCategory.EDGE_CASE,
    description="Vague ticket with insufficient information - tests handling of ambiguity",
    messages=[
        TicketMessage(
            role="customer",
            content="It's not working. Please fix it.",
            timestamp="2024-11-15T12:00:00Z",
        )
    ],
    customer_profile=CustomerProfile(
        plan="free",
        tenure_months=1,
        region="US",
        previous_tickets=0,
    ),
    expected_workflow=WorkflowExpectation(
        agents_should_include=["translator", "supervisor", "general"],
        agents_should_exclude=[],
        tools_should_include=["customer_lookup"],
        tools_should_exclude=[],
    ),
    expected_triage=TriageExpectation(
        expected_urgency=UrgencyLevel.MEDIUM,
        expected_action=RecommendedAction.ROUTE_SPECIALIST,
        expected_ticket_type="general",
        expected_sentiment="frustrated",
        should_have_kb_articles=False,
    ),
    expected_answer_criteria="""
Expected triage should:
1. Classify urgency as MEDIUM (unknown severity due to lack of detail)
2. Route to GENERAL specialist (cannot determine billing vs technical)
3. Recommend ROUTE_SPECIALIST (needs clarification from human)
4. Reasoning should acknowledge: insufficient information, needs clarification
5. Should NOT make assumptions about the specific issue
6. Suggested response should ask for more details
""",
)


# Scenario 11: Mixed Billing and Technical
MIXED_ISSUE = TriageScenario(
    id="edge-02-mixed-issue",
    name="Mixed Billing and Technical Issue",
    category=TicketCategory.EDGE_CASE,
    description="Ticket containing both billing and technical concerns - tests primary classification",
    messages=[
        TicketMessage(
            role="customer",
            content="I upgraded to Pro yesterday but the new features aren't showing up. Also, I was charged $79 but the website says Pro is $49. So I'm being overcharged AND the features I paid for don't work!",
            timestamp="2024-11-15T13:00:00Z",
        )
    ],
    customer_profile=CustomerProfile(
        plan="pro",
        tenure_months=6,
        region="US",
        previous_tickets=1,
    ),
    expected_workflow=WorkflowExpectation(
        agents_should_include=["translator", "supervisor", "billing"],
        agents_should_exclude=[],
        tools_should_include=["customer_lookup", "kb_search"],
        tools_should_exclude=[],
    ),
    expected_triage=TriageExpectation(
        expected_urgency=UrgencyLevel.HIGH,
        expected_action=RecommendedAction.ESCALATE_HUMAN,
        expected_ticket_type="billing",
        expected_sentiment="frustrated",
        should_have_kb_articles=True,
    ),
    expected_answer_criteria="""
Expected triage should:
1. Classify urgency as HIGH (overcharge + missing features)
2. Route to BILLING (primary complaint is financial)
3. Recommend ESCALATE_HUMAN (complex multi-issue case)
4. Detect frustrated sentiment (multiple problems)
5. Reasoning should acknowledge BOTH issues
6. KB search should cover: pricing, plan features, upgrade troubleshooting
""",
)


# All edge case scenarios
SCENARIOS = [AMBIGUOUS_QUERY, MIXED_ISSUE]
