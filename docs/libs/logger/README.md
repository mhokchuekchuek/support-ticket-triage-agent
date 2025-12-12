# Logger

Logging utilities for consistent logging across the project.

## Location

`libs/logger/logger.py`

## Functions

### `get_logger(name: str) -> logging.Logger`

Get a configured logger instance.

**Parameters**:
- `name`: Logger name, typically `__name__` (str)

**Returns**: Configured logger instance (logging.Logger)

**Example**:
```python
from libs.logger.logger import get_logger

logger = get_logger(__name__)
logger.info("Application started")
```

**Output**:
```
2025-12-12 10:30:45 - module_name - INFO - Application started
```

### `setup_logging(level: str = "INFO", format_type: Literal["json", "text"] = "text") -> None`

Configure logging for the application.

**Parameters**:
- `level`: Log level - DEBUG, INFO, WARNING, ERROR, CRITICAL (str, default: "INFO")
- `format_type`: Output format - "text" or "json" (Literal, default: "text")

**Returns**: None

**Example**:
```python
from libs.logger.logger import setup_logging

setup_logging(level="DEBUG", format_type="text")
```

## Usage

```python
from libs.logger.logger import get_logger, setup_logging

# Initialize logging at application startup
setup_logging(level="INFO")

# Get logger in any module
logger = get_logger(__name__)

# Use appropriate log levels
logger.debug("Diagnostic information")
logger.info("Normal operation")
logger.warning("Unexpected but recoverable")
logger.error("Operation failed", exc_info=True)
```

## Log Format

**Text format** (default):
```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

**Example output**:
```
2025-12-12 10:30:45 - src.agents.orchestrator - INFO - Agent initialized
2025-12-12 10:30:46 - src.agents.orchestrator - DEBUG - Processing request
2025-12-12 10:30:47 - src.agents.orchestrator - ERROR - Connection failed
```

## Log Levels

| Level | When to Use |
|-------|-------------|
| DEBUG | Diagnostic info for debugging |
| INFO | Normal operations, service start/stop |
| WARNING | Unexpected but recoverable situations |
| ERROR | Operation failures, exceptions |
| CRITICAL | System-wide failures |