import functools
import logging
from datetime import datetime
import time

# Standard library best practice
logger = logging.getLogger("eprofiler.auditor")
logger.addHandler(logging.NullHandler())


def audit(_func=None, *, label= "AUDIT", level=logging.INFO, include_args=False, callback=None):
    """
    A decorator that captures function execution metadata and logs the results.

    It can be used without parentheses `@audit` or with arguments `@audit(label="TASK")`.
    If no callback function passed, by default it logs to the 'eprofiler.auditor' logger.

    Args:
        _func (callable, optional): Internal parameter to support use as @audit decorator
        label (str): A custom tag to identify the audit entry (default: "AUDIT").
        level (int): The logging level to use (default: logging.INFO).
        include_args (bool): If True, captures function arguments and keyword arguments.
        callback (callable, optional): A custom function to handle the audit payload.
            If provided, logging is bypassed in favor of this function.

    Returns:
        callable: The decorated function wrapper.

    Example:
        @audit(include_args=True)
        def process_data(data):
            return data.upper()
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            payload = {
                "timestamp": datetime.now().isoformat(),
                "function": func.__qualname__,
                "label": label,
            }
            if include_args:
                payload["args"] = args
                payload["kwargs"] = kwargs
            start_time = time.perf_counter()
            try:
                result = func(*args, **kwargs)
                elapsed = time.perf_counter() - start_time
                payload["status"] = "SUCCESS"
                payload["elapsed_seconds"] = f"{elapsed:.6f}"

                if callback:
                    callback(payload)
                else:
                    logger.log(level, f"{payload}")

                return result

            except Exception as e:
                elapsed = time.perf_counter() - start_time
                payload.update({
                    "status": "FAIL",
                    "elapsed_seconds": f"{elapsed:.6f}",
                    "error": type(e).__name__,
                    "message": str(e)
                })

                if callback:
                    callback(payload)
                else:
                    logger.exception(f"{payload}")
                raise e

        return wrapper

    if _func is None:
        return decorator
    return decorator(_func)