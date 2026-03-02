import time
from functools import wraps
import tracemalloc
from typing import Callable, Any, Optional, Dict
import resource
import sys


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
        """
        Allows the Timer instance to be used as a function decorator.

        Note: When used as a decorator, results are printed to stdout
        using the label provided during initialization.
        """

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
def profile(func: Optional[Callable] = None, *, label: str = "Profile"):
    """
        A comprehensive decorator that measures wall time, CPU time, and memory usage.

        Can be used with or without parentheses:
        @profile
        @profile(label="Custom")
        """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tracemalloc.start()
            cpu_start = time.process_time()
            t0 = time.perf_counter()
            try:
                res = func(*args, **kwargs)
                t1 = time.perf_counter()
                cpu_end = time.process_time()
                current, peak = tracemalloc.get_traced_memory()
                stats = {
                    "label": label,
                    "function": func.__name__,
                    "duration": t1 - t0,  # Converted to ms for precision
                    "peak": peak,
                    "current": current,

                    "cpu_time": cpu_end - cpu_start
                }
                print(stats)
                return res

            finally:
                tracemalloc.stop()



        return wrapper

    # If func is None, it means the decorator was called with ()
    # e.g., @timer(label="Custom")
    if func is None:
        return decorator

    # If func is NOT None, it means it was called without ()
    # e.g., @timer
    return decorator(func)

# endregion


# region profile_cpu
if sys.platform != 'win32':
    def _get_cpu_stats():
        """
        Unix-specific helper to fetch process resource usage.

        Returns:
            tuple: (user_time, system_time, total_cpu_time) in seconds.
        """
        res = resource.getrusage(resource.RUSAGE_SELF)
        return res.ru_utime, res.ru_stime, (res.ru_utime + res.ru_stime)
else:  # pragma: no cover
    def _get_cpu_stats():
        """
        Windows-specific helper using process_time.

        Returns:
            tuple: (total_cpu, None, total_cpu) where None represents
                   the unavailable system-level split.
        """
        total = time.process_time()
        return total, None, total


def profile_cpu(func: Optional[Callable] = None, *, label: str = "Execution Time",
           callback: Optional[Callable[[Dict[str, Any]], None]] = None):
    """
        A deep-dive decorator for CPU consumption and execution efficiency.

        On Unix, this provides a breakdown of 'user_time' and 'system_time'.
        On Windows, it falls back to total CPU time. It calculates
        Efficiency as (cpu_time / duration * 100).

        Args:
            func: The function to be profiled.
            label: A custom string to identify the profiling run.
            callback: Optional function to handle the stats dictionary.

        Returns:
            Any: The result of the profiled function.
        """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Capture state BEFORE
            u_start, s_start, t_start = _get_cpu_stats()
            wall_start = time.perf_counter()

            result = f(*args, **kwargs)

            # Capture state AFTER
            u_end, s_end, t_end = _get_cpu_stats()
            wall_end = time.perf_counter()
            user_delta = u_end - u_start if u_start is not None else None
            sys_delta = s_end - s_start if s_start is not None else None
            cpu_total = t_end - t_start
            wall_delta = wall_end - wall_start
            efficiency = (cpu_total / wall_delta * 100) if wall_delta > 0 else 0
            stats = {
                "label": label,
                "function": f.__name__,
                "user_time": user_delta,
                "system_time": sys_delta,
                "cpu_time": cpu_total,
                "duration": wall_delta,
                "efficiency": efficiency
            }
            if callable(callback):
                callback(stats)
            else:
                print(f"{stats}")
            return result

        return wrapper

    if func is None:
        return decorator

    # If func is NOT None, it means it was called without ()
    # e.g., @timer
    return decorator(func)
# endregion