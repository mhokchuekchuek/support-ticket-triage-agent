"""Billing specialist agent for payment and subscription issues."""

from src.modules.agents.specialists.base import SpecialistBaseAgent


class BillingAgent(SpecialistBaseAgent):
    """Specialist agent for billing-related tickets.

    Handles:
    - Payment failures and processing issues
    - Refund requests and charge disputes
    - Subscription changes (upgrades, downgrades, cancellations)
    - Invoice and billing inquiries
    """

    AGENT_NAME = "BillingAgent"
    PROMPT_ID = "triage_billing"
    DOMAIN = "billing"
