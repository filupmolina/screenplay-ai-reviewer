"""
Dev Mode Logger for FastAPI

Purpose: Eliminate the "what error?" back-and-forth during debugging.

In development:
- Logs EVERYTHING with full context
- Shows request/response bodies
- Displays full stack traces
- Formats JSON nicely

In production:
- Strategic logging only
- Minimal performance impact
- Sends errors to monitoring service

Usage:
    from logger import log_request, log_response, log_error, log_debug

    @app.post("/api/tasks")
    async def create_task(task: TaskCreate):
        log_request("POST", "/api/tasks", task.dict())
        try:
            result = await db.tasks.create(task)
            log_response("POST", "/api/tasks", 201, result)
            return result
        except Exception as e:
            log_error("Task creation failed", e, {"task": task.dict()})
            raise
"""

import os
import logging
import json
import traceback
from datetime import datetime
from typing import Any, Optional, Dict

# Determine if we're in development mode
IS_DEV = os.getenv('ENV', 'development') == 'development'

# Configure logging level based on environment
logging.basicConfig(
    level=logging.DEBUG if IS_DEV else logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


def _format_json(data: Any) -> str:
    """Pretty-print JSON data"""
    try:
        if isinstance(data, (dict, list)):
            return json.dumps(data, indent=2, default=str)
        return str(data)
    except Exception:
        return str(data)


def log_request(method: str, path: str, body: Optional[Dict] = None, headers: Optional[Dict] = None):
    """
    Log incoming HTTP requests

    Args:
        method: HTTP method (GET, POST, etc.)
        path: Request path
        body: Request body (dict)
        headers: Request headers (dict)
    """
    if not IS_DEV:
        return

    logger.info(f"🔵 REQUEST {method} {path}")

    if body:
        logger.debug(f"   Body:\n{_format_json(body)}")

    if headers:
        # Don't log sensitive headers
        safe_headers = {
            k: v for k, v in headers.items()
            if k.lower() not in ['authorization', 'cookie', 'x-api-key']
        }
        if safe_headers:
            logger.debug(f"   Headers:\n{_format_json(safe_headers)}")


def log_response(method: str, path: str, status: int, data: Optional[Any] = None):
    """
    Log outgoing HTTP responses

    Args:
        method: HTTP method
        path: Request path
        status: HTTP status code
        data: Response data
    """
    if not IS_DEV:
        return

    status_emoji = "✅" if 200 <= status < 300 else "❌"
    logger.info(f"{status_emoji} RESPONSE {method} {path} - {status}")

    if data is not None:
        # Truncate large responses
        data_str = _format_json(data)
        if len(data_str) > 1000:
            data_str = data_str[:1000] + "... (truncated)"
        logger.debug(f"   Data:\n{data_str}")


def log_error(context: str, error: Exception, metadata: Optional[Dict] = None):
    """
    Log errors with full context and stack trace

    Args:
        context: Description of what was happening
        error: The exception that occurred
        metadata: Additional context (dict)
    """
    logger.error(f"❌ ERROR: {context}")
    logger.error(f"   Type: {type(error).__name__}")
    logger.error(f"   Message: {str(error)}")

    if metadata:
        logger.error(f"   Metadata:\n{_format_json(metadata)}")

    if IS_DEV:
        # Full stack trace in dev
        logger.error(f"   Stack Trace:\n{traceback.format_exc()}")
    else:
        # Abbreviated stack in production
        logger.error(f"   Stack: {traceback.format_exc(limit=3)}")

    # TODO: Send to monitoring service in production
    # if not IS_DEV:
    #     send_to_sentry(error, metadata)


def log_debug(context: str, data: Optional[Any] = None):
    """
    Debug logging - only in development

    Args:
        context: What's happening
        data: Any relevant data
    """
    if not IS_DEV:
        return

    if data is not None:
        logger.debug(f"🔍 {context}:\n{_format_json(data)}")
    else:
        logger.debug(f"🔍 {context}")


def log_state(action: str, before: Optional[Any] = None, after: Optional[Any] = None):
    """
    Log state changes (database updates, etc.)

    Args:
        action: Description of the change
        before: State before change
        after: State after change
    """
    if not IS_DEV:
        return

    logger.debug(f"📊 STATE: {action}")

    if before is not None:
        logger.debug(f"   Before:\n{_format_json(before)}")

    if after is not None:
        logger.debug(f"   After:\n{_format_json(after)}")


def log_database(operation: str, table: str, data: Optional[Any] = None):
    """
    Log database operations

    Args:
        operation: SQL operation (SELECT, INSERT, etc.)
        table: Table name
        data: Query data or results
    """
    if not IS_DEV:
        return

    logger.debug(f"💾 DATABASE {operation} {table}")

    if data is not None:
        logger.debug(f"   Data:\n{_format_json(data)}")


def log_perf(label: str, duration_ms: float, threshold: float = 1000):
    """
    Log performance metrics

    Args:
        label: Operation label
        duration_ms: Duration in milliseconds
        threshold: Threshold for "slow" warning (default 1000ms)
    """
    if not IS_DEV:
        return

    emoji = "🐌" if duration_ms > threshold else "⚡"
    logger.debug(f"{emoji} PERF: {label} took {duration_ms:.2f}ms")


def log_warn(context: str, data: Optional[Any] = None):
    """
    Log warnings - non-critical issues

    Args:
        context: What's concerning
        data: Additional context
    """
    logger.warning(f"⚠️ WARNING: {context}")

    if data is not None and IS_DEV:
        logger.warning(f"   Details:\n{_format_json(data)}")


def log_info(message: str, data: Optional[Any] = None):
    """
    General information logging

    Args:
        message: Info message
        data: Optional data
    """
    logger.info(f"ℹ️ {message}")

    if data is not None and IS_DEV:
        logger.info(f"   Data:\n{_format_json(data)}")


class PerformanceTimer:
    """
    Context manager for timing operations

    Usage:
        with PerformanceTimer("Database query"):
            result = await db.query(...)
    """

    def __init__(self, label: str):
        self.label = label
        self.start_time = None

    def __enter__(self):
        self.start_time = datetime.now()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration_ms = (datetime.now() - self.start_time).total_seconds() * 1000
            log_perf(self.label, duration_ms)


# Export all logging functions
__all__ = [
    'log_request',
    'log_response',
    'log_error',
    'log_debug',
    'log_state',
    'log_database',
    'log_perf',
    'log_warn',
    'log_info',
    'PerformanceTimer'
]
