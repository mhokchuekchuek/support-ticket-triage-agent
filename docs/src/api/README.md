# API Layer

Framework layer for HTTP interface (FastAPI).

## Overview

The API layer handles all HTTP-related concerns including routes, schemas, and dependency injection. This is the outermost layer in Clean Architecture.

## Structure

```
src/api/
├── app.py              # FastAPI application factory
├── routes/             # HTTP route handlers
│   ├── health.py
│   ├── triage.py
│   └── answer.py
├── schemas/            # Request/Response models
│   ├── requests.py
│   └── responses.py
└── dependencies/       # Dependency injection
    └── triage.py
```

## Layer Rules

| DO | DO NOT |
|----|--------|
| Handle HTTP requests/responses | Contain business logic |
| Validate request data | Access database directly |
| Call use cases (services) | Make business decisions |
| Format responses | Import from inner layers inappropriately |

## Dependencies

```
src/api/                    (Framework Layer)
    ↓ calls
src/usecases/               (Use Cases)
    ↓ uses
src/entities/               (Entities)
src/repositories/           (Repositories)
```

## Routes

| Route | File | Description |
|-------|------|-------------|
| `GET /health` | `routes/health.py` | Health check |
| `POST /api/triage` | `routes/triage.py` | Triage a support ticket |
| `POST /api/answer` | `routes/answer.py` | Save client message |

## Usage

```python
from src.api.app import create_app
from libs.configs.base import BaseConfigManager

settings = BaseConfigManager()
app = create_app(settings)
```
