"""Multi-language ticket evaluation scenarios.

Tests the triage agent's translation capabilities for non-English
tickets including language detection and meaning preservation.
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


# Scenario 8: Spanish Billing Inquiry
SPANISH_BILLING = TriageScenario(
    id="multilingual-01-spanish-billing",
    name="Spanish Language Billing Question",
    category=TicketCategory.MULTILINGUAL,
    description="Spanish language ticket about billing - tests translation accuracy and language detection",
    messages=[
        TicketMessage(
            role="customer",
            content="Hola, tengo una pregunta sobre mi factura. Veo un cargo de $99 pero mi plan deberia ser de $49 al mes. Pueden explicarme por que me cobraron mas?",
            timestamp="2024-11-15T16:00:00Z",
        )
    ],
    customer_profile=CustomerProfile(
        plan="pro",
        tenure_months=10,
        region="LATAM",
        previous_tickets=1,
    ),
    expected_workflow=WorkflowExpectation(
        agents_should_include=["translator", "supervisor", "billing"],
        agents_should_exclude=["technical"],
        tools_should_include=["customer_lookup", "kb_search"],
        tools_should_exclude=[],
    ),
    expected_triage=TriageExpectation(
        expected_urgency=UrgencyLevel.HIGH,
        expected_action=RecommendedAction.ROUTE_SPECIALIST,
        expected_ticket_type="billing",
        expected_language="es",
        expected_sentiment="confused",
        should_have_kb_articles=True,
    ),
    expected_answer_criteria="""
Expected triage should:
1. Detect language as Spanish (es)
2. Correctly translate: billing question about unexpected charge
3. Classify urgency as HIGH (billing discrepancy)
4. Route to BILLING specialist
5. Preserve original language in extracted_info
6. Translation should capture: overcharge concern, $99 vs $49 discrepancy
""",
)


# Scenario 9: Thai Technical Issue
THAI_TECHNICAL = TriageScenario(
    id="multilingual-02-thai-technical",
    name="Thai Language Technical Issue",
    category=TicketCategory.MULTILINGUAL,
    description="Thai language ticket about technical error - tests non-Latin script handling",
    messages=[
        TicketMessage(
            role="customer",
            content="สวัสดีครับ ผมมีปัญหาเรื่องการส่งออกไฟล์ PDF ระบบแสดงข้อผิดพลาด 'Export failed' ทุกครั้งที่ลอง กรุณาช่วยแก้ไขด้วยครับ",
            timestamp="2024-11-15T09:00:00Z",
        )
    ],
    customer_profile=CustomerProfile(
        plan="pro",
        tenure_months=4,
        region="APAC",
        previous_tickets=0,
    ),
    expected_workflow=WorkflowExpectation(
        agents_should_include=["translator", "supervisor", "technical"],
        agents_should_exclude=["billing"],
        tools_should_include=["customer_lookup", "kb_search"],
        tools_should_exclude=[],
    ),
    expected_triage=TriageExpectation(
        expected_urgency=UrgencyLevel.MEDIUM,
        expected_action=RecommendedAction.ROUTE_SPECIALIST,
        expected_ticket_type="technical",
        expected_language="th",
        expected_sentiment="neutral",
        should_have_kb_articles=True,
    ),
    expected_answer_criteria="""
Expected triage should:
1. Detect language as Thai (th)
2. Correctly translate: PDF export failure issue
3. Classify urgency as MEDIUM (feature not working, not blocking)
4. Route to TECHNICAL specialist
5. Find KB articles about PDF export, error troubleshooting
6. Preserve original Thai text and detect polite tone
""",
)


# All multilingual scenarios
SCENARIOS = [SPANISH_BILLING, THAI_TECHNICAL]
