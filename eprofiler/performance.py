import time
from functools import wraps
import tracemalloc
from typing import Callable, Any, Optional, Dict
import sys

if sys.platform != "win32":
    import resource
else:
    resource = None


# region timeit
def timeit(_func: Optional[Callable] = None, *, label: str = "Execution Time",
           callback: Optional[Callable[[Dict[str, Any]], None]] = None):
    """
    A decorator that measures the execution time of a function.

    Can be used without parentheses `@timeit` or with arguments `@timeit(label="TASK")`.

    Args:
        _func (Callable, optional): Internal parameter to support use as @timeit.
        label (str): A custom tag to identify the output (default: "Execution Time").
        callback (Callable, optional): A custom function to handle the stats' dictionary.
            If provided, printing to stdout is bypassed.

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
                "function": f.__qualname__,
                "duration": f"{duration:.6f}"
            }
            if callable(callback):
                callback(stats)
            else:
                print(f"{stats}")
            return result

        return wrapper

    if _func is None:
        return decorator

    return decorator(_func)

# endregion


# region Timer class
class Timer:
    """
        A multipurpose tool used as a context manager or a decorator to measure timing.

        Attributes:
            label (str): Label for the measurement.
            stats (dict): Dictionary containing the results (label and duration).
            start (float): The timestamp when the timer started.

        Example:
            with Timer("Heavy Task") as t:
                do_work()
            print(f"Total time: {t.stats['duration']}")

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
        self.start = 0.0
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
        return False

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
                "function": func.__qualname__,
                "duration": f"{duration:.6f}"
            }

            print(f"{stats}")
            return result

        return wrapper
# endregion


# region memit
def memit(_func: Optional[Callable] = None, *, label: str = "Execution Memory",
          callback: Optional[Callable[[Dict[str, Any]], None]] = None):
    """
    A decorator that measures memory usage (current and peak) during function execution.

    Can be used without parentheses `@memit` or with arguments `@memit(label="TASK")`.

    Args:
        _func (Callable, optional): Internal parameter to support use as @memit.
        label (str): A custom tag to identify the output (default: "Execution Memory").
        callback (Callable, optional): A custom function to handle the stats' dictionary.
            If provided, printing to stdout is bypassed.

    Returns:
        Callable: The decorated function or a decorator factory.
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
                    "function": f.__qualname__,
                    "current": current,
                    "peak": peak
                }
                if callable(callback):
                    callback(stats)
                else:
                    print(f"{stats}")
            return res

        return wrapper

    if _func is None:
        return decorator

    return decorator(_func)
# endregion


# region profile
def profile(_func: Optional[Callable] = None, *, label: str = "Profile",
            callback: Optional[Callable[[Dict[str, Any]], None]] = None):
    """
    A comprehensive decorator that measures wall time, CPU time, and memory usage.

    Can be used without parentheses `@profile` or with arguments `@profile(label="TASK")`.

    Args:
        _func (Callable, optional): Internal parameter to support use as @profile.
        label (str): A custom tag to identify the output (default: "Profile").
        callback (Callable, optional): A custom function to handle the stats' dictionary.
            If provided, printing to stdout is bypassed.

    Returns:
        Callable: The decorated function or a decorator factory.
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            tracemalloc.start()
            cpu_start = time.process_time()
            t0 = time.perf_counter()
            try:
                res = f(*args, **kwargs)
                t1 = time.perf_counter()
                cpu_end = time.process_time()
                current, peak = tracemalloc.get_traced_memory()
                stats = {
                    "label": label,
                    "function": f.__qualname__,
                    "duration": f"{(t1 - t0):.6f}",
                    "cpu_time": f"{(cpu_end - cpu_start):.6f}",
                    "peak": peak,
                    "current": current,
                }
                if callback:
                    callback(stats)
                else:
                    print(stats)
                return res

            finally:
                tracemalloc.stop()
        return wrapper

    if _func is None:
        return decorator

    return decorator(_func)
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
                   the unavailable system-level split for windows.
        """
        total = time.process_time()
        return total, None, total


def profile_cpu(_func: Optional[Callable] = None, *, label: str = "Execution Time",
           callback: Optional[Callable[[Dict[str, Any]], None]] = None):
    """
    A decorator for CPU time and execution efficiency.

    On Unix, this provides a breakdown of 'user_time' and 'system_time'.
    On Windows, it falls back to total CPU time. It calculates
    Efficiency as (cpu_time / duration * 100).

    Args:
        _func (Callable, optional): Internal parameter to support @profile_cpu.
        label (str): Custom tag for the profiling run (default: "CPU Profile").
        callback (Callable, optional): Custom function to handle the stats dictionary.

    Returns:
        Callable: The decorated function or a decorator factory.
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
            # Efficiency > 100% is possible on multicore systems
            efficiency = (cpu_total / wall_delta * 100) if wall_delta > 0 else 0
            stats = {
                "label": label,
                "function": f.__qualname__,
                "user_time": f"{user_delta:.6f}" if user_delta is not None else "N/A",
                "system_time": f"{sys_delta:.6f}" if sys_delta is not None else "N/A",
                "cpu_time": f"{cpu_total:.6f}",
                "duration": f"{wall_delta:.6f}",
                "efficiency": f"{efficiency:.2f}%"
            }
            if callable(callback):
                callback(stats)
            else:
                print(f"{stats}")
            return result

        return wrapper

    if _func is None:
        return decorator

    return decorator(_func)
# endregion