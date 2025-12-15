# Langfuse

## Problem

Production LLM applications need:

- End-to-end observability for multi-agent workflows
- Debugging capabilities for complex LangGraph executions
- Cost tracking per trace/session
- Prompt management with versioning
- Evaluation metrics logging for quality monitoring

## Solution

We use [Langfuse](https://langfuse.com/) as our LLM observability platform. It integrates natively with LangGraph and provides comprehensive tracing for multi-agent systems.

**Reference:** [Langfuse Documentation](https://langfuse.com/docs)

## How It Works

### LangGraph Integration

Langfuse automatically traces LangGraph workflows, showing:

- Complete execution flow (translator → supervisor → specialists)
- Token usage and costs per node
- Input/output for each agent step
- Timing breakdown for performance analysis

![LangGraph Trace in Langfuse](./assets/langfuse-langgraph-trace.png)

*The trace view shows the full multi-agent workflow with nested spans for each component.*

### Key Features Visualized

From the trace screenshot above:

1. **Hierarchical View**: Shows nested execution (LangGraph → translator → supervisor → model)
2. **Cost Tracking**: Real-time cost display per span ($0.001259 for full trace)
3. **Token Metrics**: Input/output token counts (e.g., 530 → 87 tokens)
4. **Session Linking**: Groups related traces by session/user ID
5. **Timeline**: Visual flow of agent execution with timing

## Integration with LiteLLM

Langfuse integrates seamlessly with LiteLLM proxy via callback:

```yaml
# configs/litellm/proxy_config.yaml
litellm_settings:
  success_callback: ["langfuse"]
```

Environment variables required:

```bash
LANGFUSE_PUBLIC_KEY=pk-lf-xxx
LANGFUSE_SECRET_KEY=sk-lf-xxx
LANGFUSE_HOST=https://cloud.langfuse.com  # or self-hosted URL
```

**Reference:** [LiteLLM + Langfuse Integration](https://docs.litellm.ai/docs/proxy/logging#langfuse)

## Quick Wins

### Prompt Management

Langfuse provides versioned prompt storage with labels (production, staging, etc.):

```python
from langfuse import Langfuse

langfuse = Langfuse()
prompt = langfuse.get_prompt(name="triage_supervisor", label="production")
```

**Reference:** [Prompt Management | Langfuse](https://langfuse.com/docs/prompts)

### Evaluation Scores

Log custom evaluation metrics directly to traces:

```python
langfuse.create_score(
    trace_id="trace-id",
    name="answer_quality",
    value=0.85,
    comment="LLM-as-judge evaluation"
)
```

**Reference:** [Scores | Langfuse](https://langfuse.com/docs/scores)

### Cost Analysis

Built-in cost tracking per:
- Model
- User/Session
- Time period
- Custom tags

**Reference:** [Analytics | Langfuse](https://langfuse.com/docs/analytics)

## Why Not Alternatives?

| Feature | Langfuse | LangSmith | Weights & Biases |
|---------|----------|-----------|------------------|
| LangGraph native | Yes | Yes | Limited |
| Self-host option | Yes | No | Yes |
| Prompt management | Yes | Yes | No |
| Cost tracking | Yes | Yes | Limited |
| Open source | Yes | No | No |

## Configuration

- **LiteLLM integration**: [`configs/litellm/proxy_config.yaml`](../../configs/litellm/proxy_config.yaml)
- **Evaluation config**: [`configs/evaluation.yaml`](../../configs/evaluation.yaml)
- **Observability client**: [`libs/llm/observability/langfuse/main.py`](../../libs/llm/observability/langfuse/main.py)