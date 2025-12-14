# Triage Prompts

Prompt templates for the support ticket triage system.

## Location

`prompts/triage/`

## Prompts

### Agent Prompt

`prompts/triage/agent/v1.prompt`

Main system prompt for the triage agent. Defines:
- Role and responsibilities
- Urgency classification criteria
- Action decision matrix
- Language handling
- Output JSON format

**Variables**:
- `{{ ticket_content }}` - Full ticket conversation
- `{{ customer_info }}` - Customer context

**Config**:
| Setting | Value |
|---------|-------|
| model | gpt-4o-mini |
| temperature | 0.3 |
| max_tokens | 2000 |

### Classifier Prompt

`prompts/triage/classifier/v1.prompt`

Quick classification prompt for initial ticket routing.

**Variables**:
- `{{ ticket_content }}` - Ticket message
- `{{ customer_id }}` - Customer ID
- `{{ account_type }}` - Account type

**Config**:
| Setting | Value |
|---------|-------|
| model | gpt-4o-mini |
| temperature | 0.3 |
| max_tokens | 500 |

### Responder Prompt

`prompts/triage/responder/v1.prompt`

Response generation prompt for auto-respond scenarios.

**Variables**:
- `{{ category }}` - Ticket category
- `{{ priority }}` - Ticket priority
- `{{ ticket_content }}` - Ticket content
- `{{ kb_context }}` - Relevant KB articles

**Config**:
| Setting | Value |
|---------|-------|
| model | gpt-4o-mini |
| temperature | 0.7 |
| max_tokens | 1000 |

## Urgency Levels

| Level | Criteria |
|-------|----------|
| critical | System down, data loss, security breach, enterprise outage |
| high | Major feature broken, billing errors, angry customer |
| medium | Feature questions, minor bugs, general inquiries |
| low | Feature requests, feedback, documentation questions |

## Action Matrix

| Situation | Action |
|-----------|--------|
| Clear KB answer + low/medium urgency | auto_respond |
| Technical issue | route_specialist |
| Enterprise + high urgency | escalate_human |
| Billing dispute / angry customer | escalate_human |
| Critical urgency | escalate_human |
