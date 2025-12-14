# Prompts

Prompt templates for the multi-agent triage system.

## Location

`prompts/`

## Documentation

| Document | Description |
|----------|-------------|
| [triage.md](triage.md) | Triage prompt templates |

## Structure

```
prompts/
├── __init__.py
├── uploader.py              # Syncs prompts to Langfuse
└── triage/
    ├── translator/
    │   └── v1.prompt        # Language detection and translation
    ├── supervisor/
    │   └── v1.prompt        # Classification and routing
    ├── billing/
    │   └── v1.prompt        # Billing specialist
    ├── technical/
    │   └── v1.prompt        # Technical specialist
    ├── general/
    │   └── v1.prompt        # General specialist
    ├── agent/
    │   └── v1.prompt        # (legacy) Single-agent triage
    ├── classifier/
    │   └── v1.prompt        # (legacy) Ticket classification
    └── responder/
        └── v1.prompt        # (legacy) Response generation
```

## Prompt File Format

Prompts use `.prompt` extension with YAML frontmatter:

```
---
model: gpt-4o-mini
temperature: 0.3
max_tokens: 2000
---
Your prompt content here with {{ variables }}
```

## Variables by Agent

### TranslatorAgent
- `{{ messages }}` - Ticket messages to analyze

### SupervisorAgent
- `{{ ticket_content }}` - Translated ticket content
- `{{ customer_id }}` - Customer identifier

### Specialist Agents (Billing/Technical/General)
- `{{ ticket_content }}` - Ticket messages
- `{{ customer_info }}` - Customer details
- `{{ urgency }}` - From supervisor classification
- `{{ supervisor_reasoning }}` - Classification reasoning
- `{{ original_language }}` - For response generation

## Langfuse Prompt Names

| Agent | Prompt ID |
|-------|-----------|
| TranslatorAgent | `triage_translator` |
| SupervisorAgent | `triage_supervisor` |
| BillingAgent | `triage_billing` |
| TechnicalAgent | `triage_technical` |
| GeneralAgent | `triage_general` |

## See Also

- [Prompts Config](../configs/prompts.md)
- [Multi-Agent Architecture](../decision/multi-agent-architecture.md)
