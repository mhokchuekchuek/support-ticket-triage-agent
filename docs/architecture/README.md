# Architecture

Project architecture documentation.

## Documentation

| Document | Description |
|----------|-------------|
| [code.md](code.md) | Architecture overview, layers, diagrams, patterns |
| [agent-flow.md](agent-flow.md) | Detailed step-by-step agent execution flow |

## Quick Overview

Clean Architecture with 5 layers:

```
API (src/api/) → Use Cases (src/usecases/) → Domain (src/entities/, src/modules/)
                                                    ↓
                                            Repositories (src/repositories/)
                                                    ↓
                                            Infrastructure (libs/)
```

## See Also

- [Libs](../libs/README.md)
- [Use Cases](../src/usecases/README.md)
- [Repositories](../src/repositories/README.md)
