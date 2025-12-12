# Base Selector

Base classes for the provider/selector pattern.

## Location

`libs/base/selector.py`

## Classes

### `BaseToolSelector`

Base class for tool selectors with provider-based selection.

## Usage

### Creating a Selector

Subclass `BaseToolSelector` and define `_PROVIDERS` mapping:

```python
from libs.base.selector import BaseToolSelector

class LLMClientSelector(BaseToolSelector):
    _PROVIDERS = {
        "litellm": "libs.llm.client.litellm.main.LiteLLMClient",
    }
```

### Using a Selector

```python
# Create instance with provider name and kwargs
client = LLMClientSelector.create("litellm", model="gpt-4o-mini")

# List available providers
providers = LLMClientSelector.list_providers()  # ["litellm"]
```

## Methods

### `create(provider: str, **kwargs) -> Any`

Select and instantiate tool based on provider.

**Parameters**:
- `provider`: Provider name (must be in `_PROVIDERS`)
- `**kwargs`: Provider-specific initialization parameters

**Returns**: Tool instance

**Raises**: `ValueError` if provider is unknown or class cannot be loaded

**Example**:
```python
client = LLMClientSelector.create(
    provider="litellm",
    model="gpt-4o-mini",
    api_key="sk-..."
)
```

### `list_providers() -> list[str]`

List available providers for this selector.

**Returns**: List of provider names

**Example**:
```python
providers = LLMClientSelector.list_providers()
# ["litellm"]
```

## Provider Path Format

Providers are specified as full dotted paths: `"module.path.ClassName"`

```python
_PROVIDERS = {
    "provider_name": "libs.category.subcategory.module.ClassName",
}
```

## Error Handling

The selector raises `ValueError` with descriptive messages for:
- No providers defined in subclass
- Unknown provider name
- Import failures
- Missing class in module
