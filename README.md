# Support Ticket Triage Agent

AI-powered support ticket triage using LiteLLM, LangGraph, and Qdrant hybrid search.

## Features

- **Urgency Classification**: critical/high/medium/low
- **Information Extraction**: product area, issue type, sentiment, language
- **Knowledge Base Search**: Hybrid search (semantic + BM25)
- **Action Recommendation**: auto-respond, route specialist, escalate

## Tech Stack

- **LiteLLM**: OpenAI-compatible LLM router
- **LangGraph**: Agent workflow orchestration
- **Qdrant**: Vector database with hybrid search
- **FastAPI**: REST API framework
- **Dynaconf**: Configuration management
- **Langfuse**: Observability and prompt management

## Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.10+
- OpenAI API key

### Setup

1. Clone and setup environment:

```bash
cp .env.template .env
# Edit .env with your OPENAI_API_KEY

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Start services (Qdrant, LiteLLM):

```bash
docker-compose up -d
```

3. Ingest knowledge base:

```bash
python scripts/ingest_kb.py
```

4. Run API:

```bash
uvicorn main:app --reload
```

## API Usage

### Health Check

```bash
curl http://localhost:8000/health
```

### Triage Endpoint

```bash
curl -X POST http://localhost:8000/api/triage \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "test_001",
    "customer_id": "customer_001",
    "customer_info": {
      "plan": "free",
      "tenure_months": 3,
      "region": "US",
      "previous_tickets": 1
    },
    "messages": [
      {
        "role": "customer",
        "content": "I was charged twice for my subscription!",
        "timestamp": "2024-11-15T10:30:00Z"
      }
    ]
  }'
```

### Sample Response

```json
{
  "urgency": "high",
  "extracted_info": {
    "product_area": "billing",
    "issue_type": "double charge",
    "sentiment": "frustrated",
    "language": "en"
  },
  "recommended_action": "escalate_human",
  "suggested_response": null,
  "relevant_articles": [],
  "reasoning": "Billing error with frustrated customer requires human review for refund processing"
}
```

## Architecture

Multi-agent supervisor pattern with Clean Architecture: `Entities -> Modules -> Use Cases`

```mermaid
flowchart LR
    Ticket --> Translator[TranslatorAgent]
    Translator --> Supervisor[SupervisorAgent]
    Supervisor -->|billing| Billing[BillingAgent]
    Supervisor -->|technical| Technical[TechnicalAgent]
    Supervisor -->|general| General[GeneralAgent]
    Billing --> Result[TriageResult]
    Technical --> Result
    General --> Result
```

```
src/
├── entities/           # Domain models (Ticket, TriageResult)
├── modules/
│   ├── agents/         # Multi-agent system
│   │   ├── translator.py    # Language detection/translation
│   │   ├── supervisor.py    # Classification and routing
│   │   ├── billing.py       # Billing specialist
│   │   ├── technical.py     # Technical specialist
│   │   └── general.py       # General specialist
│   └── graph/          # LangGraph workflow
└── usecases/
    └── api/            # FastAPI application
        ├── routes/     # API endpoints
        └── dependencies/  # Dependency injection
```

See [Architecture Documentation](docs/architecture/README.md) for details.

## Components

| Component | Description | Docs |
|-----------|-------------|------|
| `configs/` | Configuration files | [docs/configs](docs/configs/README.md) |
| `libs/` | Shared libraries | [docs/libs](docs/libs/README.md) |
| `ingestor/` | KB ingestion pipeline | [docs/ingestor](docs/ingestor/README.md) |
| `src/entities/` | Domain models | - |
| `src/modules/` | Agents, graph | - |
| `src/usecases/` | API layer | - |

## Documentation

- [API](docs/api/README.md)
- [Architecture](docs/architecture/README.md)
- [Configs](docs/configs/README.md)
- [Libs](docs/libs/README.md)
- [Ingestor](docs/ingestor/README.md)
- [Decisions](docs/decision/README.md)
- [Design](docs/design.md)
