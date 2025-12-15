"""Billing ticket evaluation scenarios.

Tests the triage agent's ability to correctly classify and route
billing-related support tickets with appropriate urgency levels.
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


# Scenario 1: Double Charge - High Urgency Billing
DOUBLE_CHARGE = TriageScenario(
    id="billing-01-double-charge",
    name="Double Charge Complaint",
    category=TicketCategory.BILLING,
    description="Customer reports being charged twice for subscription - HIGH urgency billing issue requiring human escalation for refund",
    messages=[
        TicketMessage(
            role="customer",
            content="I was charged twice for my subscription this month! I see two $49.99 charges on my credit card statement dated Nov 10 and Nov 12. This is unacceptable and I need an immediate refund!",
            timestamp="2024-11-15T10:30:00Z",
        )
    ],
    customer_profile=CustomerProfile(
        plan="pro",
        tenure_months=8,
        region="US",
        previous_tickets=1,
    ),
    expected_workflow=WorkflowExpectation(
        agents_should_include=["translator", "supervisor", "billing"],
        agents_should_exclude=["technical", "general"],
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
1. Classify urgency as HIGH (duplicate charges require immediate attention)
2. Route to BILLING specialist
3. Recommend ESCALATE_HUMAN (refunds require human approval)
4. Detect frustrated sentiment from language ("unacceptable", "immediate")
5. Find relevant KB articles about refund process or duplicate charges
6. Reasoning should mention: duplicate charge, refund needed, customer frustration
""",
)


# Scenario 2: Subscription Upgrade Inquiry - Medium Urgency
UPGRADE_INQUIRY = TriageScenario(
    id="billing-02-upgrade-inquiry",
    name="Plan Upgrade Question",
    category=TicketCategory.BILLING,
    description="Customer asking about upgrading plan - MEDIUM urgency billing inquiry that can be auto-responded",
    messages=[
        TicketMessage(
            role="customer",
            content="Hi, I'm currently on the Pro plan and considering upgrading to Enterprise. Can you tell me about the pricing difference and what additional features I would get? Also, would my billing cycle change?",
            timestamp="2024-11-15T14:00:00Z",
        )
    ],
    customer_profile=CustomerProfile(
        plan="pro",
        tenure_months=18,
        region="EU",
        previous_tickets=0,
    ),
    expected_workflow=WorkflowExpectation(
        agents_should_include=["translator", "supervisor", "billing"],
        agents_should_exclude=["technical"],
        tools_should_include=["customer_lookup", "kb_search"],
        tools_should_exclude=[],
    ),
    expected_triage=TriageExpectation(
        expected_urgency=UrgencyLevel.MEDIUM,
        expected_action=RecommendedAction.AUTO_RESPOND,
        expected_ticket_type="billing",
        expected_sentiment="neutral",
        should_have_kb_articles=True,
    ),
    expected_answer_criteria="""
Expected triage should:
1. Classify urgency as MEDIUM (inquiry, not blocking issue)
2. Route to BILLING specialist
3. Recommend AUTO_RESPOND (standard pricing question with KB coverage)
4. Detect neutral/positive sentiment (polite inquiry)
5. Find KB articles about plan comparison, enterprise features, billing cycles
6. Provide suggested response explaining upgrade process
""",
)


# All billing scenarios
SCENARIOS = [DOUBLE_CHARGE, UPGRADE_INQUIRY]
