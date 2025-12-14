# LLM Module

LLM-related utilities and integrations.

## Location

`libs/llm/`

## Submodules

| Submodule | Purpose | Documentation |
|-----------|---------|---------------|
| Client | LLM provider clients | [client/README.md](client/README.md) |
| Chunking | Text chunking strategies | [chunking/README.md](chunking/README.md) |
| Observability | LLM tracing and monitoring | [observability/README.md](observability/README.md) |
| Prompt Manager | Centralized prompt management | [prompt_manager/README.md](prompt_manager/README.md) |

## Architecture

```text
libs/llm/
├── client/           # LLM provider clients
│   ├── base.py       # BaseLLM abstract class
│   ├── selector.py   # LLMClientSelector
│   ├── litellm/      # HTTP-based client
│   └── langchain/    # ChatOpenAI wrapper
├── chunking/         # Text chunking strategies
│   ├── base.py       # BaseChunker abstract class
│   ├── selector.py   # TextChunkerSelector
│   └── recursive/    # Recursive text splitter
├── observability/    # LLM tracing
│   ├── base.py       # BaseObservability abstract class
│   ├── selector.py   # ObservabilitySelector
│   └── langfuse/     # Langfuse tracing
└── prompt_manager/   # Prompt management
    ├── base.py       # BasePromptManager abstract class
    ├── selector.py   # PromptManagerSelector
    └── langfuse/     # Langfuse prompts
```
