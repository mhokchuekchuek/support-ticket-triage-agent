# Architecture

## Clean Architecture Layers

```mermaid
flowchart TB
    subgraph API["API Layer (src/api/)"]
        Routes[Routes]
        Dependencies[Dependencies]
    end

    subgraph UseCases["Use Cases (src/usecases/)"]
        TriageService[TriageService]
    end

    subgraph Domain["Domain (src/)"]
        Entities[Entities]
        Agents[Agents]
        Workflow[Workflow]
    end

    subgraph Repositories["Repositories (src/repositories/)"]
        CheckpointRepo[CheckpointRepository]
        TicketRepo[TicketRepository]
        ChatRepo[ChatRepository]
    end

    subgraph Infrastructure["Infrastructure (libs/)"]
        LLMClient[LLM Client]
        VectorStore[Vector Store]
        SQLClient[SQL Client]
        KVClient[KeyValue Client]
    end

    Routes --> UseCases
    UseCases --> Domain
    UseCases --> Repositories
    Repositories --> Infrastructure
    Domain --> Entities
```

| Layer | Folder | Responsibility |
|-------|--------|---------------|
| API | `src/api/` | HTTP handlers, dependency injection |
| Use Cases | `src/usecases/` | Application business logic orchestration |
| Domain | `src/entities/`, `src/modules/` | Core business rules, agents, workflow |
| Repositories | `src/repositories/` | Abstract data persistence |
| Infrastructure | `libs/` | Database clients, external APIs |

## Project Structure

```
support-ticket-triage-agent/
├── main.py                      # Entry point (config injection)
├── configs/                     # YAML configuration files
│   ├── agents/
│   ├── litellm/
│   └── prompts/
├── libs/                        # Infrastructure layer
│   ├── database/
│   │   ├── keyvalue_db/         # Redis client
│   │   ├── tabular/sql/         # PostgreSQL client
│   │   └── vector/              # Qdrant client
│   ├── llm/
│   │   ├── client/              # LiteLLM client
│   │   ├── observability/       # Langfuse
│   │   └── prompt_manager/
│   └── logger/
├── src/
│   ├── entities/                # Domain models
│   ├── modules/                 # Domain logic
│   │   ├── agents/              # Agent implementations
│   │   └── graph/               # LangGraph workflow
│   ├── usecases/                # Use Cases (services)
│   │   └── triage/              # TriageService
│   ├── api/                     # API layer
│   │   ├── routes/
│   │   └── dependencies/
│   ├── repositories/            # Data access abstraction
│   │   ├── checkpoint/
│   │   ├── ticket/
│   │   └── chat/
│   └── configs/                 # Settings (Dynaconf)
└── docs/                        # Documentation
```

## System Architecture

```mermaid
flowchart TB
    subgraph Client
        API[FastAPI /api/triage]
    end

    subgraph Workflow["LangGraph Multi-Agent Workflow"]
        Start([Start]) --> Translator[Translator Agent]
        Translator --> Supervisor[Supervisor Agent]
        Supervisor --> Route{Route Decision}
        Route -->|billing| Billing[Billing Agent]
        Route -->|technical| Technical[Technical Agent]
        Route -->|general| General[General Agent]
        Route -->|escalate| Escalate[Direct Escalation]
        Billing --> End([End])
        Technical --> End
        General --> End
        Escalate --> End
    end

    subgraph External["External Services"]
        LLM[LiteLLM / OpenAI]
        Qdrant[(Qdrant Vector DB)]
        Langfuse[Langfuse Observability]
        Redis[(Redis Checkpointer)]
    end

    API --> Workflow
    Translator --> LLM
    Supervisor --> LLM
    Billing --> LLM
    Technical --> LLM
    General --> LLM
    Billing --> Qdrant
    Technical --> Qdrant
    General --> Qdrant
    Workflow --> Langfuse
    Workflow --> Redis
```

## Component Flow

```mermaid
sequenceDiagram
    participant Client
    participant API as FastAPI
    participant Service as TriageService
    participant Workflow as MultiAgentWorkflow
    participant Translator as TranslatorAgent
    participant Supervisor as SupervisorAgent
    participant Specialist as SpecialistAgent
    participant KB as KBRetrievalTool
    participant Customer as CustomerLookupTool
    participant Repos as Repositories
    participant LLM as LiteLLM

    Client->>API: POST /api/triage
    API->>Service: triage_ticket(ticket)
    Note over Service: Pre-workflow: Ticket matching
    Service->>Repos: scan_activated_ticket_ids()
    Service->>Workflow: invoke(ticket, config)
    Workflow->>Translator: execute(state)
    Translator->>LLM: detect language, translate
    LLM-->>Translator: TranslationResult
    Translator-->>Workflow: state with translation
    Workflow->>Supervisor: execute(state)
    Supervisor->>Customer: lookup(customer_id)
    Customer-->>Supervisor: customer info
    Supervisor->>LLM: classify urgency/type
    LLM-->>Supervisor: SupervisorDecision
    Supervisor-->>Workflow: state with decision
    Workflow->>Specialist: execute(state)
    Specialist->>KB: search(query, category)
    KB-->>Specialist: relevant articles
    Specialist->>LLM: generate triage result
    LLM-->>Specialist: TriageResult
    Specialist-->>Workflow: final state
    Workflow-->>Service: result
    Note over Service: Post-workflow: Persist if completed
    Service->>Repos: save_ticket(), save_messages()
    Service-->>API: result
    API-->>Client: JSON response
```

## Data Flow

```mermaid
flowchart LR
    subgraph Input
        Ticket[Ticket Model]
    end

    subgraph Translation
        Detect[Detect Language]
        Translate[Translate to English]
    end

    subgraph Classification
        Lookup[Customer Lookup]
        Classify[Classify Urgency/Type]
        Route[Route to Specialist]
    end

    subgraph Specialist
        Search[KB Search]
        Analyze[Domain Analysis]
        Recommend[Recommend Action]
    end

    subgraph Output
        Result[TriageResult Model]
    end

    Ticket --> Detect
    Detect --> Translate
    Translate --> Lookup
    Lookup --> Classify
    Classify --> Route
    Route --> Search
    Search --> Analyze
    Analyze --> Recommend
    Recommend --> Result
```

## Module Dependencies

```mermaid
flowchart TB
    subgraph API["API Layer"]
        Routes[Routes]
        Dependencies[Dependencies]
    end

    subgraph Services["Use Cases"]
        TriageService
    end

    subgraph Repositories
        CheckpointRepo[CheckpointRepository]
        TicketRepo[TicketRepository]
        ChatRepo[ChatRepository]
    end

    subgraph Domain
        subgraph Entities
            Ticket
            TriageResult
        end

        subgraph Workflow
            MultiAgentWorkflow
        end

        subgraph Agents
            Translator[Translator Agent]
            Supervisor[Supervisor Agent]
            Billing[Billing Agent]
            Technical[Technical Agent]
            General[General Agent]
        end

        subgraph Tools
            KBTool[KB Retrieval Tool]
            CustomerTool[Customer Lookup Tool]
        end
    end

    subgraph Libs["Infrastructure"]
        LLMClient[LLM Client]
        VectorStore[Vector Store]
        SQLClient[SQL Client]
        KVClient[KeyValue Client]
        PromptManager[Prompt Manager]
        Observability
        Config
    end

    Routes --> TriageService
    TriageService --> MultiAgentWorkflow
    TriageService --> CheckpointRepo
    TriageService --> TicketRepo
    TriageService --> ChatRepo
    MultiAgentWorkflow --> Translator
    MultiAgentWorkflow --> Supervisor
    MultiAgentWorkflow --> Billing
    MultiAgentWorkflow --> Technical
    MultiAgentWorkflow --> General
    Supervisor --> CustomerTool
    Billing --> KBTool
    Technical --> KBTool
    General --> KBTool
    Translator --> LLMClient
    Supervisor --> LLMClient
    Billing --> LLMClient
    Technical --> LLMClient
    General --> LLMClient
    KBTool --> VectorStore
    CustomerTool --> SQLClient
    CheckpointRepo --> KVClient
    TicketRepo --> SQLClient
    ChatRepo --> SQLClient
    Dependencies --> Config
    Dependencies --> Observability
```

## Agent Responsibilities

| Agent | Tools | Purpose |
|-------|-------|---------|
| TranslatorAgent | None | Language detection and translation |
| SupervisorAgent | customer_lookup | Classification and routing |
| BillingAgent | kb_search (billing) | Billing domain expertise |
| TechnicalAgent | kb_search (technical) | Technical domain expertise |
| GeneralAgent | kb_search (general) | General inquiry handling |

## Design Decisions

- **Config injection via main.py** - Configuration loaded once at startup
- **FastAPI app factory pattern** - `create_app(config)` receives config dict
- **Dynaconf for settings** - Environment-aware configuration
- **Provider pattern for libs** - Swappable implementations
- **Repository pattern** - Abstracts data access from business logic
- **Service layer** - Orchestrates pre/post workflow logic

## Key Files

| File | Purpose |
|------|---------|
| `main.py` | Entry point, config injection |
| `src/api/app.py` | FastAPI application factory |
| `src/api/dependencies/triage.py` | Service initialization |
| `src/usecases/triage/main.py` | TriageService |
| `src/modules/graph/workflow.py` | MultiAgentWorkflow |

## See Also

- [Agent Flow](agent-flow.md) - Detailed step-by-step execution flow
