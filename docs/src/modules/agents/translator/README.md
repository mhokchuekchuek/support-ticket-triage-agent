# TranslatorAgent

Agent for language detection and translation.

## Location

`src/modules/agents/translator/main.py`

## Overview

Runs first in the workflow to ensure all downstream agents work with English text:
- Detects the original language of ticket messages
- Translates non-English content to English
- Preserves original messages for response generation

## Class

```python
class TranslatorAgent(BaseAgent):
    def __init__(
        self,
        llm,
        observability: Optional[any] = None,
        prompt_manager: Optional[any] = None,
        agent_config: Optional[dict] = None,
    ):
        ...
```

## Tools

None - uses direct LLM invocation for translation.

## Usage

```python
from src.modules.agents.translator.main import TranslatorAgent

agent = TranslatorAgent(
    llm=llm,
    prompt_manager=prompt_manager,
    agent_config=config,
)
```

## Output

Returns `TranslationResult`:
- `original_language`: Detected language code (e.g., "th", "es", "en")
- `is_english`: Whether the content is already in English
- `translated_messages`: Translated content (if non-English)
- `original_messages`: Original preserved messages

## See Also

- [BaseAgent](../base.md)
- [Agent Flow](../../graph/agent-flow.md)
