"""General inquiry evaluation scenarios.

Tests the triage agent's ability to correctly classify and route
general support tickets such as feature questions and account inquiries.
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


# Scenario 5: Feature Question - Low Urgency
FEATURE_QUESTION = TriageScenario(
    id="general-01-feature-question",
    name="Feature Availability Question",
    category=TicketCategory.GENERAL,
    description="Customer asking about product features - LOW urgency general inquiry that can be auto-responded",
    messages=[
        TicketMessage(
            role="customer",
            content="Hello! I was wondering if your platform supports integration with Slack? I'd like to receive notifications about important updates directly in our team channels. Also, is there documentation on how to set this up?",
            timestamp="2024-11-15T15:30:00Z",
        )
    ],
    customer_profile=CustomerProfile(
        plan="pro",
        tenure_months=3,
        region="US",
        previous_tickets=0,
    ),
    expected_workflow=WorkflowExpectation(
        agents_should_include=["translator", "supervisor", "general"],
        agents_should_exclude=["billing"],
        tools_should_include=["customer_lookup", "kb_search"],
        tools_should_exclude=[],
    ),
    expected_triage=TriageExpectation(
        expected_urgency=UrgencyLevel.LOW,
        expected_action=RecommendedAction.AUTO_RESPOND,
        expected_ticket_type="general",
        expected_sentiment="neutral",
        should_have_kb_articles=True,
    ),
    expected_answer_criteria="""
Expected triage should:
1. Classify urgency as LOW (informational inquiry, not blocking)
2. Route to GENERAL specialist
3. Recommend AUTO_RESPOND (feature documentation question)
4. Detect neutral/positive sentiment (friendly inquiry with greeting)
5. Find KB articles about integrations, Slack setup, notifications
6. Provide suggested response with documentation links
""",
)


# All general scenarios
SCENARIOS = [FEATURE_QUESTION]
