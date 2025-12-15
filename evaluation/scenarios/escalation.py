"""Escalation scenario evaluations.

Tests the triage agent's ability to correctly identify situations
requiring immediate human escalation such as legal threats and data loss.
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


# Scenario 6: Legal Threat
LEGAL_THREAT = TriageScenario(
    id="escalation-01-legal-threat",
    name="Legal Threat from Customer",
    category=TicketCategory.ESCALATION,
    description="Customer threatening legal action - requires immediate escalation regardless of issue type",
    messages=[
        TicketMessage(
            role="customer",
            content="This is completely unacceptable. I've been charged for 6 months for a service I cancelled. If I don't receive a full refund of $594 within 48 hours, I will be contacting my lawyer and filing a complaint with the Better Business Bureau.",
            timestamp="2024-11-15T15:00:00Z",
        )
    ],
    customer_profile=CustomerProfile(
        plan="pro",
        tenure_months=12,
        region="US",
        previous_tickets=5,
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
        expected_ticket_type="billing",
        expected_sentiment="angry",
        should_have_kb_articles=False,
    ),
    expected_answer_criteria="""
Expected triage should:
1. Classify urgency as CRITICAL (legal threat triggers escalation)
2. Set requires_escalation=true (legal/regulatory concern)
3. Recommend ESCALATE_HUMAN immediately
4. Detect angry sentiment from language
5. Reasoning must mention: legal threat, BBB complaint, multiple disputes
6. Should NOT attempt auto-response
""",
)


# Scenario 7: Data Loss Report
DATA_LOSS = TriageScenario(
    id="escalation-02-data-loss",
    name="Potential Data Loss",
    category=TicketCategory.ESCALATION,
    description="Customer reporting data appears deleted - critical security/data issue requiring immediate escalation",
    messages=[
        TicketMessage(
            role="customer",
            content="All my project files are gone! I logged in this morning and my entire workspace is empty. I had 2 years worth of work in there. This cannot be happening - where is my data?!",
            timestamp="2024-11-15T07:00:00Z",
        )
    ],
    customer_profile=CustomerProfile(
        plan="enterprise",
        tenure_months=26,
        region="EU",
        seats=20,
        previous_tickets=2,
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
        expected_sentiment="panicked",
        should_have_kb_articles=False,
    ),
    expected_answer_criteria="""
Expected triage should:
1. Classify urgency as CRITICAL (data loss is highest priority)
2. Set requires_escalation=true (data loss requires immediate engineering)
3. Recommend ESCALATE_HUMAN
4. Detect panicked/distressed sentiment
5. Reasoning should cite: data loss risk, enterprise customer, 2 years of data
6. Enterprise + data loss = immediate escalation
""",
)


# All escalation scenarios
SCENARIOS = [LEGAL_THREAT, DATA_LOSS]
