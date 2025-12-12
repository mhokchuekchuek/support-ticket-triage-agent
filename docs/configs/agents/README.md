# Agent Configurations

Agent-specific configurations with LLM settings.

## Location

`configs/agents/`

## Table of Contents

| Agent | Description | Config File |
|-------|-------------|-------------|
| [Triage](triage.md) | Support ticket triage agent | `configs/agents/triage.yaml` |

## Structure

Each agent config follows this pattern:

```yaml
<agent_name>:
  llm:
    provider: "litellm"
    model: "<model_name>"
    temperature: <float>
    max_tokens: <int>

  vectordb:
    collection_name: "<collection>"
```

## Supported Models

Available models are configured in [`configs/litellm/proxy_config.yaml`](../../../configs/litellm/proxy_config.yaml). For the full list of LiteLLM supported models, see [LiteLLM Providers](https://docs.litellm.ai/docs/providers).

## Adding New Agents

1. Create `configs/agents/<agent_name>.yaml`
2. Add documentation at `docs/configs/agents/<agent_name>.md`
3. Update this README table of contents
