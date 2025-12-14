# BillingAgent

Specialist agent for billing-related support tickets.

## Location

`src/modules/agents/billing.py`

## Class

### `BillingAgent`

Extends `SpecialistBaseAgent` for billing domain expertise.

**Class Attributes**:

| Attribute | Value |
|-----------|-------|
| `AGENT_NAME` | "BillingAgent" |
| `PROMPT_ID` | "triage_billing" |
| `DOMAIN` | "billing" |

## Handles

- Payment failures and declined transactions
- Refund requests
- Subscription changes (upgrades/downgrades)
- Invoice questions
- Billing cycle inquiries
- Charge disputes

## Tools

- **kb_search**: Searches knowledge base filtered by `category=billing`

## Configuration

```yaml
triage:
  agents:
    billing:
      prompt:
        id: triage_billing
        environment: production
      category_filter: billing
```

## Output

Returns `TriageResult` with billing-specific analysis:

```python
TriageResult(
    urgency=UrgencyLevel.HIGH,
    extracted_info=ExtractedInfo(
        product_area="billing",
        issue_type="payment_failure",
        sentiment="frustrated",
        language="en",
    ),
    recommended_action=RecommendedAction.ROUTE_SPECIALIST,
    reasoning="Customer payment failed, needs billing team review",
)
```
