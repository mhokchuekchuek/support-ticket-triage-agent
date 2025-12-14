# GeneralAgent

Specialist agent for general support inquiries.

## Location

`src/modules/agents/general.py`

## Class

### `GeneralAgent`

Extends `SpecialistBaseAgent` for general domain expertise.

**Class Attributes**:

| Attribute | Value |
|-----------|-------|
| `AGENT_NAME` | "GeneralAgent" |
| `PROMPT_ID` | "triage_general" |
| `DOMAIN` | "general" |

## Handles

- Feature questions and how-to guidance
- Account settings and preferences
- Product documentation requests
- Feature requests and feedback
- General inquiries

## Tools

- **kb_search**: Searches knowledge base filtered by `category=general`

## Configuration

```yaml
triage:
  agents:
    general:
      prompt:
        id: triage_general
        environment: production
      category_filter: general
```

## Output

Returns `TriageResult` with general analysis:

```python
TriageResult(
    urgency=UrgencyLevel.LOW,
    extracted_info=ExtractedInfo(
        product_area="general",
        issue_type="feature_question",
        sentiment="neutral",
        language="en",
    ),
    recommended_action=RecommendedAction.AUTO_RESPOND,
    reasoning="Simple feature question, can be answered from KB",
)
```
