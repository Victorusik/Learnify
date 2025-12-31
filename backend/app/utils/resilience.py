import logging
import asyncio
from functools import wraps
from sqlalchemy.exc import OperationalError, DisconnectionError
from typing import Callable, Any, Type, Tuple

logger = logging.getLogger(__name__)

def retry_db_operation(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 10.0,
    backoff_factor: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (OperationalError, DisconnectionError)
):
    """
    Decorator to retry database operations with exponential backoff.
    """
    def decorator(func: Callable[..., Any]):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_retries:
                        logger.error(f"Operation failed after {max_retries} retries: {e}")
                        raise last_exception
                    
                    logger.warning(f"Database operation failed (attempt {attempt + 1}/{max_retries}). Retrying in {delay}s... Error: {e}")
                    await asyncio.sleep(delay)
                    delay = min(delay * backoff_factor, max_delay)
            
            # Should not be reached
            raise last_exception

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
             # Basic sync implementation if needed, though FastAPI is mostly async
             # For blocking DB calls (common with SQLAlchemy ORM without asyncio ext)
             # We might need time.sleep instead of asyncio.sleep
            import time
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_retries:
                        logger.error(f"Operation failed after {max_retries} retries: {e}")
                        raise last_exception
                    
                    logger.warning(f"Database operation failed (attempt {attempt + 1}/{max_retries}). Retrying in {delay}s... Error: {e}")
                    time.sleep(delay)
                    delay = min(delay * backoff_factor, max_delay)
            raise last_exception

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
            
    return decorator
