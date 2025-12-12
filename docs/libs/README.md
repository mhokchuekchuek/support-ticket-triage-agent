# Libs Module

Reusable utilities and external service integrations.

## Categories

| Category | Purpose | Documentation |
|----------|---------|---------------|
| Base | Base classes for provider pattern | [base/README.md](base/README.md) |
| LLM | LLM provider integrations | [llm/README.md](llm/README.md) |
| Database | Database and vector store clients | [database/README.md](database/README.md) |
| Logger | Logging utilities | [logger/README.md](logger/README.md) |

## Provider Pattern

### Purpose
Swappable implementations for external services.

### Structure
- **Base Class**: Abstract interface defining common methods
- **Selector**: Factory for provider selection via registry
- **Providers**: Concrete implementations

### Benefits
- Easy testing with mocks
- Switch providers without code changes
- Consistent interface across providers

## Adding New Providers

### Steps
1. Create provider implementation inheriting from base class
2. Register in selector's `_PROVIDERS` registry
3. Configure provider name in settings
4. Create documentation file for the new provider
