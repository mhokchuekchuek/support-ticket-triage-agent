# LLM Module

LLM-related utilities and integrations.

## Location

`libs/llm/`

## Submodules

| Submodule | Purpose | Documentation |
|-----------|---------|---------------|
| Client | LLM provider clients | [client/README.md](client/README.md) |
| Chunking | Text chunking strategies | [chunking/README.md](chunking/README.md) |

## Architecture

```text
libs/llm/
├── client/           # LLM provider clients
│   ├── base.py       # BaseLLM abstract class
│   ├── selector.py   # LLMClientSelector
│   ├── litellm/      # HTTP-based client
│   └── langchain/    # ChatOpenAI wrapper
└── chunking/         # Text chunking strategies
    ├── base.py       # BaseChunker abstract class
    ├── selector.py   # TextChunkerSelector
    └── recursive/    # Recursive text splitter
```
