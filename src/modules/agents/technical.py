"""Technical specialist agent for system and access issues."""

from src.modules.agents.specialist_base import SpecialistBaseAgent


class TechnicalAgent(SpecialistBaseAgent):
    """Specialist agent for technical-related tickets.

    Handles:
    - System errors and outages (HTTP errors, downtime)
    - Access and login issues
    - Performance problems
    - Bug reports
    - Regional/infrastructure issues
    """

    AGENT_NAME = "TechnicalAgent"
    PROMPT_ID = "triage_technical"
    DOMAIN = "technical"
