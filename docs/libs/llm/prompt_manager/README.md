# Prompt Manager

Centralized prompt management using the provider/selector pattern.

## Location

`libs/llm/prompt_manager/`

## Providers

| Provider | Description | Documentation |
|----------|-------------|---------------|
| `langfuse` | Langfuse Cloud prompts | [langfuse.md](langfuse.md) |

## Classes

### BasePromptManager

Abstract base class for prompt managers.

**Location**: `libs/llm/prompt_manager/base.py`

**Methods**:

| Method | Description |
|--------|-------------|
| `get_prompt(name, version, label)` | Retrieve prompt from backend |
| `upload_prompt(name, prompt, config, labels)` | Upload prompt to backend |
| `is_available()` | Check if backend is available |

### PromptManagerSelector

Selector for prompt manager providers.

**Location**: `libs/llm/prompt_manager/selector.py`

**Methods**:

| Method | Description |
|--------|-------------|
| `create(provider, **kwargs)` | Create client instance |
| `list_providers()` | List available providers |
