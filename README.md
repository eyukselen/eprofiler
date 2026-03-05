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
* **`@memit`**: Simple peak memory tracking using `tracemalloc`.
* **`@profile` / `@profile_cpu`**: Combined time, memory, and CPU profiling.
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

@audit(label="PAYMENT_GATEWAY", include_args=True)
def process_payment(user_id, amount):
    # Logic here...
    return True

process_payment(123, 50.0)
```
**Output (Standard Logging):**
> INFO: {'timestamp': '2026-03-02T10:00:00.123', 'function': 'process_payment', 'label': 'PAYMENT_GATEWAY', 'args': (123, 50.0), 'status': 'SUCCESS', 'elapsed_seconds': '0.045200'}

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

> {'label': 'Computation', 'function': 'my_func', 'duration': 0.008421}

### 3. Comprehensive Profiling (`@profile`)
Track time and memory (current and peak) simultaneously.

```python
from eprofiler import profile

@profile(label="Heavy Task")
def memory_intensive():
    return [x for x in range(1000000)]

memory_intensive()
```

**Output:** 
> {'label': 'Heavy Task', 'function': 'memory_intensive', 'duration': 0.041200, 'peak': 324502, 'current': 1204}

### 4. Advanced: Callbacks & Custom Capture
Instead of printing to the console, you can capture results programmatically.

```python
from eprofiler import audit

def my_db_callback(payload):
    # Send payload to Datadog, Slack, or a Database
    print(f"Captured: {payload['status']} in {payload['elapsed_seconds']}s")

@audit(callback=my_db_callback)
def sync_data():
    pass
```

---

## Links
* **PyPI**: [https://pypi.org/project/eprofiler/](https://pypi.org/project/eprofiler/)
* **GitHub**: [https://github.com/eyukselen/eprofiler](https://github.com/eyukselen/eprofiler)
* **Docs**: [https://eprofiler.readthedocs.io](https://eprofiler.readthedocs.io)

---