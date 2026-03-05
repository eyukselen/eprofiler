# eprofiler

**A lightweight, zero-dependency toolkit to monitor execution of functions or code blocks.**

[![PyPI](https://img.shields.io/pypi/v/eprofiler.svg?color=blue)](https://pypi.org/project/eprofiler/)
[![Build Status](https://github.com/eyukselen/eprofiler/actions/workflows/python-tests.yml/badge.svg)](https://github.com/eyukselen/eprofiler/actions)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://readthedocs.org/projects/eprofiler/badge/?version=latest)](https://eprofiler.readthedocs.io/en/latest/?badge=latest)


`eprofiler` provides decorators and context managers to observe execution time, cpu time, peak memory and arguments used for a function.  

for a function or code block you can monitor and log;
* execution time
* peak memory usage
* CPU time
* parameters passed to a function

## Installation

```bash
pip install eprofiler
```

## Core Tools

* **`@audit`**: Execution logging with `SUCCESS`/`FAIL` status and error capturing.
* **`@timeit`**: Execution timing (microsecond precision).
* **`@memit`**: Tracks current and peak memory usage.
* **`@profile`**: The "All-in-One": Wall time, CPU time, and Memory. 
* **`@profile_cpu`**: User vs System time (Unix) & Efficiency %.
* **`Timer`**: Context manager and/or decorator for granular blocks.

---

## Usage

### 1. Function Auditing (`@audit`)
Good for monitoring what parameters are passed to a function/method.
where you need to know if a function finished, how long it took, and why it failed and with which parameters.

> &#9888; Warning:   
> if parameters passed to function are not printable like `str`, `int` or 
> a python object without `__str__` or `__repr__` that can be used in fstrings
> its better to use callback to handle them in logging

```python
from eprofiler import audit

@audit(label="Audit", include_args=True)
def create_user(username, email):
    return f"User {username} created."
```
**Output:**
> INFO: {'timestamp': '2026-03-05T18:33:37.651931', 'function': 'create_user', 'label': 'Audit', 'args': ('jdoe', 'jane@example.com'), 'kwargs': {}, 'status': 'SUCCESS', 'elapsed_seconds': '0.000003'}

### 2. Basic Timing (`@timeit`)
For quick performance checks during development. By default, results are printed to the console.

```python
from eprofiler import timeit

@timeit(label="Computation")
def my_func():
    return sum(i**2 for i in range(100000))

my_func()
```

**Output:** 

> {'label': 'Computation', 'function': 'my_func', 'duration': '0.000074'}

### 3. Comprehensive Profiling (`@profile` & `@profile_cpu`)
Track wall-clock time, actual CPU usage, and memory (current and peak) simultaneously.

```python
from eprofiler import profile, profile_cpu

# Standard profile (Wall Time + CPU Time + Memory)
@profile(label="Data Batch")
def process_data():
    return [x for x in range(1000000)]

# CPU profile (User/System breakdown + Efficiency)
@profile_cpu(label="Heavy Computation")
def compute_pi():
    return sum(1/i**2 for i in range(1, 1000000))

process_data()
compute_pi()
```

**Output:**
> {'label': 'Data Batch', 'function': 'process_data', 'duration': '0.241128', 'cpu_time': '0.241104', 'peak': 40440488, 'current': 40440448}
> 
> {'label': 'Heavy Computation', 'function': 'compute_pi', 'user_time': '0.048526', 'system_time': '0.000074', 'cpu_time': '0.048600', 'duration': '0.048610', 'efficiency': '99.98%'}


### 4. Using Callback 
Instead of printing to the console, you can pass a callback function to any decorator 
to handle the results programmatically (e.g., sending metrics to a database, Slack, or a logging service).

```python
from eprofiler import profile_cpu

def metrics_handler(stats):
    """Custom function to process profiling data."""
    # Send to Datadog, CloudWatch, or an ELK stack
    print(f"TELEMETRY: {stats['function']} ran with {stats['efficiency']} efficiency.")

@profile_cpu(label="Production_Task", callback=metrics_handler)
def sync_data():
    # Logic here...
    return "Done"

sync_data()
```
Using your own `metrics_handler` you can do anything you want with stats.

### 5. Timer class for codeblocks
Timer can be used as a decoator, or can be used for code blocks for part of a function rather than whole function
Note that `Timer` class does not have a callback

```python
from eprofiler import Timer
import time

# Use as a Context Manager
with Timer(label="External API Call") as t:
    time.sleep(0.5)  # Simulate a network delay

print(f"Result: {t.stats['label']} took {t.stats['duration']:.6f}s")

# Also works as a decorator for simple timing
@Timer(label="Quick Check")
def short_task():
    pass
```

---

## Links
* **PyPI**: [https://pypi.org/project/eprofiler/](https://pypi.org/project/eprofiler/)
* **GitHub**: [https://github.com/eyukselen/eprofiler](https://github.com/eyukselen/eprofiler)
* **Docs**: [https://eprofiler.readthedocs.io](https://eprofiler.readthedocs.io)

---