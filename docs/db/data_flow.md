# Data Flow

This document describes how data flows between the three database systems in the Support Ticket Triage Agent.

## Complete Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           DATA FLOW OVERVIEW                             │
└─────────────────────────────────────────────────────────────────────────┘

1. USER SUBMITS TICKET
   POST /api/triage { ticket_id, customer_id, messages[] }
                    ↓
2. WORKFLOW EXECUTION
   ┌──────────────────────────────────────────────────────────────┐
   │  TicketMatcherAgent                                          │
   │  └─ READS Redis: Scan for customer's active tickets          │
   │                                                              │
   │  TranslatorAgent → Language detection                        │
   │                                                              │
   │  SupervisorAgent                                             │
   │  └─ READS PostgreSQL: CustomerLookupTool (customers table)   │
   │                                                              │
   │  Specialist Agent → READS Qdrant for KB articles             │
   │                                                              │
   │  Each step WRITES to Redis checkpoint                        │
   └──────────────────────────────────────────────────────────────┘
                    ↓
3. USER SENDS FOLLOW-UP (Optional)
   POST /api/answer { ticket_id, content }
   └─ UPDATES Redis: Append HumanMessage to checkpoint
   └─ Workflow resumes from checkpoint
                    ↓
4. TICKET COMPLETED
   ┌──────────────────────────────────────────────────────────────┐
   │  TicketPersistenceAgent                                      │
   │                                                              │
   │  A. WRITES PostgreSQL:                                       │
   │     - INSERT chat_messages (all conversation)                │
   │                                                              │
   │  B. DELETES Redis:                                           │
   │     - Cleanup checkpoint keys                                │
   └──────────────────────────────────────────────────────────────┘
                    ↓
5. RESPONSE RETURNED
   TriageResult { urgency, suggested_response, ... }
```

## Database Operations by Component

### Write Operations

| Component | Database | Operation | Table/Key |
|-----------|----------|-----------|-----------|
| LangGraph | Redis | SET | `langgraph:session:*` |
| `/api/answer` endpoint | Redis | UPDATE | Append to checkpoint |
| TicketPersistenceAgent | PostgreSQL | INSERT | `chat_messages` |

### Read Operations

| Component | Database | Operation | Purpose |
|-----------|----------|-----------|---------|
| TicketMatcherAgent | Redis | SCAN | Find customer's active tickets |
| CustomerLookupTool | PostgreSQL | SELECT | Get customer data |
| KBRetrievalTool | Qdrant | SEARCH | Semantic KB article lookup |

### Delete Operations

| Component | Database | Operation | When |
|-----------|----------|-----------|------|
| TicketPersistenceAgent | Redis | DELETE | After PostgreSQL save |

## Redis Checkpointing

### Purpose
Redis serves as "hot storage" for active workflows, enabling:
- Multi-turn conversations
- Human-in-the-loop interactions
- Workflow resumption

### Key Pattern
```
langgraph:session:{customer_id}:{ticket_id}:*
```

### Checkpoint Structure
```python
{
    "v": 1,
    "id": ticket_id,
    "ts": timestamp,
    "channel_values": {
        "messages": [HumanMessage, AIMessage, ...],
        "ticket": {...},
        "translation": {...},
        "supervisor_decision": {...},
        "triage_result": {...}
    },
    "channel_versions": {},
    "versions_seen": {}
}
```

### Lifecycle

1. **Created**: When workflow starts for a new ticket
2. **Updated**: After each agent step
3. **Appended**: When user sends follow-up via `/api/answer`
4. **Deleted**: When ticket is completed and saved to PostgreSQL

## Dual Persistence Strategy

```
┌─────────────────────┐     ┌─────────────────────┐
│   HOT STORAGE       │     │   COLD STORAGE      │
│   (Redis)           │     │   (PostgreSQL)      │
├─────────────────────┤     ├─────────────────────┤
│ • Fast, in-memory   │ ──► │ • Durable           │
│ • Active workflows  │     │ • Queryable         │
│ • Ephemeral         │     │ • Analytics ready   │
│ • Checkpointing     │     │ • Permanent records │
└─────────────────────┘     └─────────────────────┘
          │
          └──► Data moves from Redis to PostgreSQL
               when ticket is completed
```

## Qdrant (Vector Database)

### Purpose
Stores knowledge base article embeddings for semantic search.

### Collection Structure
- **Vector Dimension**: 1536 (OpenAI embeddings)
- **Distance Metric**: Cosine similarity

### Search Flow
1. Query text → LLM embedding (1536 dimensions)
2. Vector search in Qdrant with optional category filter
3. Returns top-k articles with similarity scores

### Category Filters
Each specialist agent searches only their domain:
- `BillingAgent` → `category: "billing"`
- `TechnicalAgent` → `category: "technical"`
- `GeneralAgent` → `category: "general"`

## Sequence Diagram: Complete Ticket Flow

```
User        API         Redis       PostgreSQL    Qdrant
 │           │            │             │           │
 │──POST────►│            │             │           │
 │  /triage  │            │             │           │
 │           │──SCAN─────►│             │           │
 │           │◄───────────│             │           │
 │           │            │             │           │
 │           │──SELECT───►│─────────────►           │
 │           │  customers │             │           │
 │           │◄───────────│─────────────│           │
 │           │            │             │           │
 │           │────────────│─────────────│──SEARCH──►│
 │           │            │             │           │
 │           │◄───────────│─────────────│◄──────────│
 │           │            │             │           │
 │           │──SET──────►│  (checkpoint)           │
 │           │◄───────────│             │           │
 │           │            │             │           │
 │           │──INSERT───►│─────────────►           │
 │           │  chat_msgs │             │           │
 │           │◄───────────│─────────────│           │
 │           │            │             │           │
 │           │──DELETE───►│  (cleanup)  │           │
 │           │◄───────────│             │           │
 │           │            │             │           │
 │◄──200─────│            │             │           │
 │  Result   │            │             │           │
```
