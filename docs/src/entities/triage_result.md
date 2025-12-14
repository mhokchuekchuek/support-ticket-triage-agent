# Triage Result Models

Triage analysis output models for the support ticket system.

## Location

`src/entities/triage_result.py`

## Enums

### `UrgencyLevel`

Urgency classification levels.

| Value | Description |
|-------|-------------|
| `CRITICAL` | Requires immediate attention |
| `HIGH` | Urgent, should be addressed soon |
| `MEDIUM` | Normal priority |
| `LOW` | Can be addressed when convenient |

### `RecommendedAction`

Recommended triage actions.

| Value | Description |
|-------|-------------|
| `AUTO_RESPOND` | Can be handled with automated response |
| `ROUTE_SPECIALIST` | Route to specialist team |
| `ESCALATE_HUMAN` | Escalate to human agent |

## Classes

### `ExtractedInfo`

Information extracted from ticket analysis.

**Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `product_area` | str | No | Product area affected |
| `issue_type` | str | Yes | Type of issue |
| `sentiment` | str | Yes | Customer sentiment |
| `language` | str | No | Detected language (default: "en") |

### `RelevantArticle`

Knowledge base article reference.

**Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | str | Yes | Article unique identifier |
| `title` | str | Yes | Article title |
| `relevance_score` | float | Yes | Relevance score (0-1) |

### `TriageResult`

Triage analysis output model.

**Fields**:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `urgency` | UrgencyLevel | Yes | Urgency classification |
| `extracted_info` | ExtractedInfo | Yes | Extracted information |
| `recommended_action` | RecommendedAction | Yes | Recommended action |
| `suggested_response` | str | No | Suggested response text |
| `relevant_articles` | list[RelevantArticle] | No | Relevant KB articles (default: []) |
| `reasoning` | str | Yes | Explanation for the triage decision |

## Usage

```python
from src.entities.triage_result import (
    TriageResult,
    UrgencyLevel,
    RecommendedAction,
    ExtractedInfo,
    RelevantArticle
)

# Create triage result
result = TriageResult(
    urgency=UrgencyLevel.CRITICAL,
    extracted_info=ExtractedInfo(
        product_area="billing",
        issue_type="payment_failure",
        sentiment="frustrated",
        language="en"
    ),
    recommended_action=RecommendedAction.ESCALATE_HUMAN,
    suggested_response="I apologize for the billing issues...",
    relevant_articles=[
        RelevantArticle(
            id="KB-001",
            title="Payment Troubleshooting Guide",
            relevance_score=0.92
        )
    ],
    reasoning="Multiple failed charges with escalating frustration. Customer threatening chargeback."
)
```
