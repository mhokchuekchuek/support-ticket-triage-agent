# Multi-Agent Supervisor Architecture

## Problem

Single-agent triage has limitations:

- **One prompt handles everything**: Classification, KB search, response generation all in one prompt leads to complexity and inconsistency
- **No domain specialization**: Generic prompts cannot capture billing vs technical vs general expertise
- **Non-English tickets**: No dedicated handling for language detection and translation
- **Difficult to maintain**: Changing one aspect (e.g., billing logic) risks breaking others
- **Limited observability**: Hard to trace which part of triage failed

## Solution

We use a **multi-agent supervisor pattern** with specialized agents:

```
Ticket -> Translator -> Supervisor -> [Billing|Technical|General] -> TriageResult
```

**Reference:** [LangGraph Multi-Agent Concepts](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/concepts/multi_agent.md#supervisor)

## Why Supervisor Pattern?

We evaluated three multi-agent patterns:

| Pattern | Description | Pros | Cons |
|---------|-------------|------|------|
| **Network** | Agents communicate freely | Flexible | Hard to debug, unpredictable flow |
| **Hierarchical** | Multiple supervisor levels | Scales well | Overkill for our use case |
| **Supervisor** | Single router to specialists | Clear flow, easy to trace | Single point of routing |

**Decision:** Supervisor pattern fits our needs:
- Clear, predictable flow for ticket triage
- Easy to add new specialist agents
- Simple to debug and trace
- Each agent has single responsibility

## Agent Responsibilities

| Agent | Tools | Why Separate |
|-------|-------|--------------|
| **TranslatorAgent** | None | Language detection needs to happen first; translated content used by all downstream agents |
| **SupervisorAgent** | customer_lookup | Classification needs customer context; routing decision is a distinct concern |
| **BillingAgent** | kb_search (billing) | Domain expertise with billing-specific KB and prompts |
| **TechnicalAgent** | kb_search (technical) | Domain expertise with technical-specific KB and prompts |
| **GeneralAgent** | kb_search (general) | Catch-all for non-billing, non-technical issues |

## Why Translation First?

Non-English tickets must be translated before:
1. **Supervisor classification** - LLM performs better classifying English text
2. **KB search** - Knowledge base is in English
3. **Response generation** - Specialists generate English response, can be translated back

## Why Category-Based KB Filtering?

We considered two approaches for specialist KB access:

| Approach | Description | Pros | Cons |
|----------|-------------|------|------|
| **Multiple collections** | Separate Qdrant collections per domain | Strict isolation | Complex ingestion, more infrastructure |
| **Category filtering** | Single collection with metadata filter | Simple, single ingestion pipeline | Slightly larger index |

**Decision:** Category-based filtering with single `knowledge_base` collection:
- Simpler to maintain
- Single ingestion pipeline
- Filter by `category` metadata at search time
- Each specialist passes its domain category to `kb_search`

## Benefits

1. **Separation of concerns**: Each agent does one thing well
2. **Domain expertise**: Specialist prompts capture domain knowledge
3. **Easier testing**: Test each agent independently
4. **Better observability**: Trace shows which agent handled what
5. **Extensibility**: Add new specialists without changing existing ones
6. **Language support**: Dedicated translation preserves original for response

## Trade-offs

1. **More LLM calls**: 3 agents minimum per ticket (translator, supervisor, specialist)
2. **Latency**: Sequential flow adds latency vs single-agent
3. **Complexity**: More code to maintain than single agent

**Mitigation:**
- Use faster models (gpt-4o-mini) for translator/supervisor
- Redis checkpointing enables resumption on failure
- Clear agent boundaries make maintenance easier

## Configuration

See [`configs/agents/triage.yaml`](../../configs/agents/triage.yaml) for agent configurations.

## See Also

- [MultiAgentWorkflow](../src/modules/graph/workflow.md)
- [Agent Documentation](../src/modules/agents/README.md)
