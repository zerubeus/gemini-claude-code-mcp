"""Logging configuration for Gemini-Claude Code MCP server."""

import asyncio
import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional

import structlog
from rich.console import Console
from rich.logging import RichHandler

from gemini_claude_code_mcp.config import settings


def setup_logging(level: Optional[str] = None, log_file: Optional[str] = None, use_rich: bool = True) -> None:
    """Set up logging configuration.

    Args:
        level: Logging level (overrides settings)
        log_file: Log file path (overrides settings)
        use_rich: Whether to use rich console for pretty output
    """
    # Use settings or provided values
    log_level = level or settings.logging.level
    log_file_path = log_file or settings.logging.file

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt='iso'),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.CallsiteParameterAdder(
                parameters=[
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                ]
            ),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Console handler
    if use_rich:
        console = Console(stderr=True)
        console_handler = RichHandler(console=console, rich_tracebacks=True, tracebacks_show_locals=True, markup=True)
    else:
        console_handler = logging.StreamHandler(sys.stderr)

    console_handler.setLevel(getattr(logging, log_level))
    console_formatter = structlog.stdlib.ProcessorFormatter(processor=structlog.dev.ConsoleRenderer(colors=use_rich))
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # File handler if specified
    if log_file_path:
        log_path = Path(log_file_path)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.handlers.RotatingFileHandler(
            log_path,
            maxBytes=settings.logging.max_file_size_mb * 1024 * 1024,
            backupCount=settings.logging.backup_count,
        )
        file_handler.setLevel(getattr(logging, log_level))

        file_formatter = structlog.stdlib.ProcessorFormatter(processor=structlog.processors.JSONRenderer())
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

    # Set up specific loggers
    for logger_name in ['mcp', 'gemini_claude_code_mpc']:
        logger = logging.getLogger(logger_name)
        logger.setLevel(getattr(logging, log_level))
        logger.propagate = True


def get_logger(name: str) -> structlog.BoundLogger:
    """Get a configured logger instance.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)


class LogContext:
    """Context manager for temporary log context."""

    def __init__(self, **kwargs):
        """Initialize with context variables."""
        self.context = kwargs
        self._tokens = []

    def __enter__(self):
        """Enter context and bind variables."""
        for key, value in self.context.items():
            token = structlog.contextvars.bind_contextvars(**{key: value})
            self._tokens.append(token)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context and clear variables."""
        for token in self._tokens:
            structlog.contextvars.unbind_contextvars(token)


def log_performance(func):
    """Decorator to log function performance."""
    import functools
    import time

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        start_time = time.time()

        try:
            result = await func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info('Function completed', function=func.__name__, duration=f'{duration:.3f}s', status='success')
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                'Function failed', function=func.__name__, duration=f'{duration:.3f}s', status='error', error=str(e)
            )
            raise

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        start_time = time.time()

        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info('Function completed', function=func.__name__, duration=f'{duration:.3f}s', status='success')
            return result
        except Exception as e:
            duration = time.time() - start_time
            logger.error(
                'Function failed', function=func.__name__, duration=f'{duration:.3f}s', status='error', error=str(e)
            )
            raise

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
