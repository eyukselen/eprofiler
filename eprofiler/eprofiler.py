import time
from functools import wraps
import tracemalloc
from typing import Callable, Any, Optional, Dict


# region timeit
def timeit(func: Optional[Callable] = None, *, label: str = "Execution Time",
           callback: Optional[Callable[[Dict[str, Any]], None]] = None):
    """
    A decorator that measures the execution time of a function.

    Can be used with or without parentheses.

    Args:
        func (Callable, optional): The function to monitor. Defaults to None.
        label (str): A label to identify the output. Defaults to "Execution Time".
        callback (Callable, optional): A function to handle the stats dictionary.
            If None, results are printed to stdout. Defaults to None.

    Returns:
        Callable: The wrapped function or the decorator itself.
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            local_f = f
            if not args and not kwargs:
                start = time.perf_counter()
                result = local_f()
                duration = time.perf_counter()- start
            else:
                start = time.perf_counter()
                result = local_f(*args, **kwargs)
                duration = time.perf_counter() - start

            stats = {
                "label": label,
                "function": f.__name__,
                "duration": duration
            }
            if callable(callback):
                callback(stats)
            else:
                print(f"{stats}")
            return result

        return wrapper

    # If func is None, it means the decorator was called with ()
    # e.g., @timer(label="Custom")
    if func is None:
        return decorator

    # If func is NOT None, it means it was called without ()
    # e.g., @timer
    return decorator(func)

# endregion


# region Timer class
class Timer:
    """
    A multi-purpose tool used as a context manager or a decorator to measure timing.

    Example::

        with Timer("Heavy Task") as t:
            do_work()

        @Timer("My Function")
        def my_func():
            pass
    """

    def __init__(self, label: str = "Execution"):
        """
        Initialize the Timer.

        Args:
            label (str): Label for the measurement. Defaults to "Execution".
        """
        self.label = label
        self.stats: dict[str, Any] = {
            "label": label,
            "duration": None
        }

    # Context Manager Logic
    def __enter__(self):
        """Starts the timer when entering the context."""
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stops the timer and records duration on exit."""
        duration = time.perf_counter() - self.start
        self.stats["duration"] = duration
        # print(f"{self.stats}")
        return False  # Let exceptions propagate

    def __call__(self, func: Callable):
        """Allows the class to be used as a function decorator."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            local_f = func
            if not args and not kwargs:
                start = time.perf_counter()
                result = local_f()
                duration = time.perf_counter()- start
            else:
                start = time.perf_counter()
                result = local_f(*args, **kwargs)
                duration = time.perf_counter() - start
            stats = {
                "label": self.label,
                "function": func.__name__,
                "duration": duration
            }

            print(f"{stats}")
            return result

        return wrapper

# endregion


# region memit
def memit(func: Optional[Callable] = None, label: str = "Execution Memory",
          callback: Optional[Callable[[Dict[str, Any]], None]] = None):
    """
    A decorator that measures memory usage (current and peak) during function execution.

    Args:
        func (Callable, optional): The function to monitor. Defaults to None.
        label (str): Label for the output. Defaults to "Execution Memory".
        callback (Callable, optional): Function to handle results dictionary.
            Defaults to None.

    Returns:
        Callable: The wrapped function.
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            current, peak = 0, 0
            tracemalloc.start()
            try:
                res = f(*args, **kwargs)
                current, peak = tracemalloc.get_traced_memory()
            finally:
                tracemalloc.stop()
                stats = {
                    "label": label,
                    "function": f.__name__,
                    "current": current,
                    "peak": peak
                }
                if callable(callback):
                    callback(stats)
                else:
                    print(f"{stats}")
            return res

        return wrapper

    if func is None:
        return decorator
    return decorator(func)

# endregion

# region profile
def profile(label: str = "Profile"):
    """
    A comprehensive decorator that measures both time and memory usage.

    Args:
        label (str): Label for the report. Defaults to "Profile".

    Returns:
        Callable: The decorator function.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tracemalloc.start()
            t0 = time.perf_counter()
            try:
                res = func(*args, **kwargs)
                t1 = time.perf_counter()
                current, peak = tracemalloc.get_traced_memory()
            finally:
                tracemalloc.stop()
            stats = {
                "label": label,
                "function": func.__name__,
                "duration": t1 - t0,  # Converted to ms for precision
                "peak": peak,
                "current": current
            }
            print(stats)
            return res

        return wrapper

    return decorator

# endregion