# Evaluation System

LLM-as-a-Judge evaluation framework for the Support Ticket Triage Agent.

## Overview

The evaluation system measures triage accuracy, workflow compliance, and response quality using:

1. **Deterministic Metrics** - Exact match comparisons (urgency, routing, action)
2. **Workflow Validation** - Verifies correct agents/tools via Langfuse traces
3. **LLM-as-a-Judge** - GPT-4 evaluates reasoning quality and completeness

## Architecture

```text
evaluation/
├── evaluator.py           # Main orchestrator
├── llm_judge.py           # LLM-based quality scoring
├── workflow_validator.py  # Agent/tool validation via Langfuse
├── config.py              # Configuration loader
└── scenarios/             # Test scenarios by category
    ├── base.py            # Dataclass definitions
    ├── billing.py         # Billing ticket scenarios
    ├── technical.py       # Technical ticket scenarios
    ├── general.py         # General inquiry scenarios
    ├── escalation.py      # Escalation scenarios
    ├── multilingual.py    # Multi-language scenarios
    └── edge_cases.py      # Edge case scenarios
```

## Quick Start

### 1. Set Environment Variables

```bash
export EVALUATION_API_URL=http://localhost:8000
export LANGFUSE_SECRET_KEY=sk-lf-4e5c96fc-9480-46cc-9c45-9a029c366937
export LANGFUSE_PUBLIC_KEY=pk-lf-9d2b56dd-d9e4-40ef-a1a5-6594fd5aef33
export LANGFUSE_HOST=https://cloud.langfuse.com
export LITELLM_PROXY_URL=http://litellm-proxy:4000
export LITELLM_API_KEY=sk-1234
```

### 2. Upload Evaluation Prompts to Langfuse

```bash
python scripts/upload_evaluation_prompts.py --label production
```

### 3. Run Evaluation

```bash
# Run all scenarios
python scripts/run_triage_evaluation.py

# Run specific category
python scripts/run_triage_evaluation.py --category billing

# Save results to file
python scripts/run_triage_evaluation.py --output results/eval-2024-11-15.json
```

## Test Scenarios

| ID | Category | Urgency | Action | Description |
|----|----------|---------|--------|-------------|
| billing-01 | billing | HIGH | ESCALATE_HUMAN | Double charge complaint |
| billing-02 | billing | MEDIUM | AUTO_RESPOND | Plan upgrade inquiry |
| technical-01 | technical | CRITICAL | ESCALATE_HUMAN | Enterprise system outage |
| technical-02 | technical | HIGH | ROUTE_SPECIALIST | Repeated login failures |
| general-01 | general | LOW | AUTO_RESPOND | Feature availability question |
| escalation-01 | escalation | CRITICAL | ESCALATE_HUMAN | Legal threat |
| escalation-02 | escalation | CRITICAL | ESCALATE_HUMAN | Data loss report |
| multilingual-01 | multilingual | HIGH | ROUTE_SPECIALIST | Spanish billing question |
| multilingual-02 | multilingual | MEDIUM | ROUTE_SPECIALIST | Thai technical issue |
| edge-01 | edge_cases | MEDIUM | ROUTE_SPECIALIST | Ambiguous query |
| edge-02 | edge_cases | HIGH | ESCALATE_HUMAN | Mixed billing/technical |

## Metrics

### Classification Accuracy (Deterministic)

| Metric | Description | Scale |
|--------|-------------|-------|
| `urgency_accuracy` | Urgency level match | 0 or 1 |
| `routing_accuracy` | Ticket type routing match | 0 or 1 |
| `action_accuracy` | Recommended action match | 0 or 1 |
| `language_accuracy` | Language detection match | 0 or 1 |

### Workflow Validation

| Metric | Description |
|--------|-------------|
| `agents.pass` | Required agents were invoked |
| `agents.missing` | Expected agents not found |
| `agents.unwanted` | Excluded agents that were used |
| `tools.pass` | Required tools were called |
| `tools.missing` | Expected tools not called |

### Quality Scores (LLM Judge, 0-1 scale)

| Metric | Description |
|--------|-------------|
| `answer_quality` | Reasoning clarity and professionalism |
| `factual_correctness` | Accuracy of classifications |
| `completeness` | Coverage of expected criteria |
| `language_detection` | Correct language identified |
| `translation_accuracy` | Meaning preserved in translation |
| `articles_found` | KB article retrieval success |
| `relevance_quality` | KB article relevance to issue |

## Evaluation Flow

```text
┌─────────────────────────────────────────────────────────────┐
│                    For Each Scenario                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  1. Build Ticket Payload                                    │
│     - customer_id, ticket_id                                │
│     - customer_info (plan, tenure, region)                  │
│     - messages (customer content)                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  2. POST to /api/triage                                     │
│     - Send ticket payload                                   │
│     - Receive TriageResult                                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  3. Wait for Langfuse Trace (30s default)                   │
│     - Traces submitted asynchronously                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  4. Classification Accuracy (Deterministic)                 │
│     - Compare urgency, action, type, language               │
│     - Exact match = 1.0, mismatch = 0.0                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  5. Workflow Validation                                     │
│     - Fetch trace from Langfuse                             │
│     - Extract agents and tools from observations            │
│     - Compare against scenario expectations                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  6. Quality Evaluation (LLM Judge)                          │
│     - Load prompt from Langfuse                             │
│     - Fill template with scenario + result                  │
│     - GPT-4 scores: quality, correctness, completeness      │
│     - Log scores to Langfuse                                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  7. Aggregate Results                                       │
│     - Store all metrics per scenario                        │
│     - Print summary statistics                              │
└─────────────────────────────────────────────────────────────┘
```

## Configuration

### configs/evaluation.yaml

```yaml
evaluation:
  api_url: "http://localhost:8000"

  llm:
    provider: "litellm"
    model: "gpt-4"
    temperature: 0.0
    max_tokens: 2000

  observability:
    langfuse:
      host: "https://cloud.langfuse.com"

  workflow:
    trace_wait_time: 30  # seconds
    max_retries: 10
    retry_delay: 3

  thresholds:
    answer_quality: 0.7
    factual_correctness: 0.8
    urgency_accuracy: 0.9
```

## Evaluation Prompts

Prompts are stored in Langfuse for versioning and easy updates.

| Prompt Name | Purpose |
|-------------|---------|
| `evaluation_triage_quality` | Overall triage quality assessment |
| `evaluation_translation` | Translation accuracy for non-English |
| `evaluation_kb_relevance` | KB article relevance scoring |

### Prompt Template Variables

**triage_quality:**
- `{{scenario_name}}`, `{{scenario_description}}`
- `{{ticket_messages}}`, `{{customer_profile}}`
- `{{expected_criteria}}`
- `{{actual_result}}`
- `{{expected_urgency}}`, `{{expected_action}}`, `{{expected_type}}`

## Adding New Scenarios

1. Create scenario in appropriate category file (`evaluation/scenarios/*.py`):

```python
from evaluation.scenarios.base import (
    TriageScenario, WorkflowExpectation, TriageExpectation,
    CustomerProfile, TicketMessage, TicketCategory
)
from src.entities.triage_result import UrgencyLevel, RecommendedAction

NEW_SCENARIO = TriageScenario(
    id="category-XX-name",
    name="Human Readable Name",
    category=TicketCategory.BILLING,  # or TECHNICAL, GENERAL, etc.
    description="What this scenario tests",
    messages=[
        TicketMessage(
            role="customer",
            content="Customer message content",
            timestamp="2024-11-15T10:00:00Z"
        )
    ],
    customer_profile=CustomerProfile(
        plan="pro",
        tenure_months=12,
        region="US",
        previous_tickets=2
    ),
    expected_workflow=WorkflowExpectation(
        agents_should_include=["translator", "supervisor", "billing"],
        agents_should_exclude=["technical"],
        tools_should_include=["customer_lookup", "kb_search"],
        tools_should_exclude=[]
    ),
    expected_triage=TriageExpectation(
        expected_urgency=UrgencyLevel.HIGH,
        expected_action=RecommendedAction.ESCALATE_HUMAN,
        expected_ticket_type="billing",
        expected_language="en",
        expected_sentiment="frustrated",
        should_have_kb_articles=True
    ),
    expected_answer_criteria="""
    Expected triage should:
    1. ...
    2. ...
    """
)

# Add to SCENARIOS list
SCENARIOS = [..., NEW_SCENARIO]
```

1. Run evaluation to test:

```bash
python scripts/run_triage_evaluation.py --scenario category-XX-name
```

## Output Example

```text
[1/11] Running: Double Charge Complaint (billing)
  -> Sending ticket to API...
  -> Session ID: eval-billing-01-double-charge-20241115-103000
  -> Waiting 30s for trace submission...
  -> Evaluating classification accuracy...
  -> Classification: urgency=OK, routing=OK, action=OK
  -> Validating workflow...
  -> Workflow: PASS
  -> Evaluating quality with LLM judge...
  -> Quality: answer=0.85, factual=0.90, complete=0.80

============================================================
EVALUATION SUMMARY
============================================================

Total Scenarios: 11
Successful Runs: 11/11
Workflow Passed: 10/11

Classification Accuracy:
  Urgency:  90.9%
  Routing:  100.0%
  Action:   90.9%

Quality Scores (avg):
  Answer Quality: 0.82

By Category:
  billing: 2/2 success, 100.0% urgency accuracy
  technical: 2/2 success, 100.0% urgency accuracy
  general: 1/1 success, 100.0% urgency accuracy
  escalation: 2/2 success, 100.0% urgency accuracy
  multilingual: 2/2 success, 100.0% urgency accuracy
  edge_cases: 2/2 success, 50.0% urgency accuracy
============================================================
```

## Langfuse Integration

### Traces

Each evaluation run creates a trace with:
- `session_id`: `eval-{scenario_id}-{timestamp}`
- Observations for each agent and tool call
- Linked evaluation scores

### Scores

Scores are logged to Langfuse automatically:
- `triage_quality_answer_quality`
- `triage_quality_factual_correctness`
- `triage_quality_completeness`
- `triage_quality_overall` (average)
- `translation_*` (for multilingual scenarios)
- `kb_relevance_*` (for scenarios with KB search)

View scores in Langfuse dashboard under the trace's session.

## Troubleshooting

### "Evaluation prompt not found in Langfuse"

Upload prompts first:

```bash
python scripts/upload_evaluation_prompts.py --label production
```

### "Could not fetch trace from Langfuse"

- Increase wait time: `--wait-time 60`
- Check Langfuse credentials
- Verify API is using same Langfuse project

### "API request timed out"

- Check API is running: `curl http://localhost:8000/health`
- Increase timeout in evaluator.py (default: 120s)

### Low classification accuracy

- Review scenario expectations match current agent behavior
- Check if agent prompts have changed
- Verify KB articles are indexed
