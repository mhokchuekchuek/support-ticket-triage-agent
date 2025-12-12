# Support Ticket Triage Agent

AI-powered support ticket triage system using LangGraph and FastAPI.

## Quick Start

### Prerequisites

- Python 3.11+
- Docker (for Qdrant, Redis, PostgreSQL)

### Installation

```bash
pip install -r requirements.txt
```

### Environment Setup

```bash
cp .env.template .env
```

Add your OpenAI API key to `.env`:

```bash
OPENAI_API_KEY=sk-...
```

### Run Services

```bash
docker-compose up -d
```

### Start API

```bash
uvicorn main:app --reload
```

### Test

```bash
curl http://localhost:8000/health
```

## Architecture

Clean Architecture: `Entities → Modules → Use Cases`

See [Architecture Documentation](docs/architecture/README.md) for details.

## Components

| Component | Description | Docs |
|-----------|-------------|------|
| `configs/` | Configuration files | [docs/configs](docs/configs/README.md) |
| `libs/` | Shared libraries | [docs/libs](docs/libs/README.md) |
| `src/configs/` | Settings class | [docs/configs/settings.md](docs/configs/settings.md) |
| `src/entities/` | Domain models | - |
| `src/modules/` | Agents, graph | - |
| `src/usecases/` | API layer | - |

## Documentation

- [Architecture](docs/architecture/README.md)
- [Configs](docs/configs/README.md)
- [Libs](docs/libs/README.md)
- [Decisions](docs/decision/README.md)
