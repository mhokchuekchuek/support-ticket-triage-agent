# TechnicalAgent

Specialist agent for technical support tickets.

## Location

`src/modules/agents/technical.py`

## Class

### `TechnicalAgent`

Extends `SpecialistBaseAgent` for technical domain expertise.

**Class Attributes**:

| Attribute | Value |
|-----------|-------|
| `AGENT_NAME` | "TechnicalAgent" |
| `PROMPT_ID` | "triage_technical" |
| `DOMAIN` | "technical" |

## Handles

- System errors and crashes
- Login/authentication issues
- Performance problems
- API integration issues
- Data sync failures
- Service outages

## Tools

- **kb_search**: Searches knowledge base filtered by `category=technical`

## Configuration

```yaml
triage:
  agents:
    technical:
      prompt:
        id: triage_technical
        environment: production
      category_filter: technical
```

## Output

Returns `TriageResult` with technical analysis:

```python
TriageResult(
    urgency=UrgencyLevel.CRITICAL,
    extracted_info=ExtractedInfo(
        product_area="technical",
        issue_type="system_error",
        sentiment="frustrated",
        language="en",
    ),
    recommended_action=RecommendedAction.ESCALATE_HUMAN,
    reasoning="Critical system error affecting enterprise customer",
)
```
