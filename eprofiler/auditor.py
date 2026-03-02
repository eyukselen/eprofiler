import functools
import logging
from datetime import datetime
import time

# Standard library best practice
logger = logging.getLogger("eprofiler.auditor")
logger.addHandler(logging.NullHandler())


def audit(_func=None, *, label= "AUDIT", level=logging.INFO, include_args=False, callback=None):
    """
    Captures function execution metadata.
    Works as @audit or @audit(include_args=True).
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


                # Execution of the "Audit"
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