"""General specialist agent for feature and account inquiries."""

from src.modules.agents.specialists.base import SpecialistBaseAgent


class GeneralAgent(SpecialistBaseAgent):
    """Specialist agent for general inquiries.

    Handles:
    - Feature questions and how-to guidance
    - Account settings and preferences
    - Product documentation and tutorials
    - Feature requests and feedback
    """

    AGENT_NAME = "GeneralAgent"
    PROMPT_ID = "triage_general"
    DOMAIN = "general"
