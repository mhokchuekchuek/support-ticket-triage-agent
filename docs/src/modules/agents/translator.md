# TranslatorAgent

Agent responsible for language detection and translation of non-English tickets.

## Location

`src/modules/agents/translator.py`

## Class

### `TranslatorAgent`

Detects the language of incoming tickets and translates non-English content to English for downstream processing.

**Attributes**:

| Attribute | Type | Description |
|-----------|------|-------------|
| `llm` | BaseLLM | LLM client for translation |
| `observability` | LangfuseObservability | Observability wrapper for tracing |
| `prompt_manager` | BasePromptManager | Prompt manager for loading prompts |
| `agent_config` | dict | Agent configuration from YAML |
| `system_prompt` | str | Loaded from prompt_manager |

## Methods

### `__init__(llm, observability, prompt_manager, agent_config)`

Initialize the translator agent.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `llm` | BaseLLM | LLM client with chat capability |
| `observability` | LangfuseObservability | For tracing LLM calls |
| `prompt_manager` | BasePromptManager | For loading prompts |
| `agent_config` | dict | Configuration with prompt ID |

### `execute(state: AgentState) -> AgentState`

Detect language and translate if needed.

**Parameters**:

| Parameter | Type | Description |
|-----------|------|-------------|
| `state` | AgentState | Current state with ticket |

**Returns**: Updated state with `translation` field containing `TranslationResult`.

## Configuration

```yaml
# configs/agents/triage.yaml
triage:
  agents:
    translator:
      prompt:
        id: triage_translator
        environment: production
```

## Prompt

Langfuse prompt: `triage_translator`

**Variables**:
- `{{ messages }}`: Ticket messages to analyze

## Output

Adds `TranslationResult` to state:

```python
TranslationResult(
    original_language="th",
    is_english=False,
    translated_messages=["Translated content..."],
    original_messages=["Original Thai content..."]
)
```

## Usage

```python
from src.modules.agents.translator import TranslatorAgent

translator = TranslatorAgent(
    llm=llm_client,
    observability=observability,
    prompt_manager=prompt_manager,
    agent_config=config.agents.translator,
)

# Used in workflow
state = translator.execute(state)
```
