"""Evaluation scenarios for triage testing.

Provides test scenarios organized by category for comprehensive evaluation
of the triage agent's classification, routing, and response quality.
"""

from evaluation.scenarios import (
    billing,
    technical,
    general,
    escalation,
    multilingual,
    edge_cases,
)

__all__ = [
    "billing",
    "technical",
    "general",
    "escalation",
    "multilingual",
    "edge_cases",
]
