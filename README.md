# eprofiler

**Modern Execution, Memory & Audit Profiler for Python**

A lightweight, zero-dependency toolkit to monitor performance and audit function lifecycles. 
`eprofiler` provides high-precision decorators and context managers to identify bottlenecks and log execution metadata with minimal friction.

[![PyPI version](https://img.shields.io/pypi/v/eprofiler.svg)](https://pypi.org/project/eprofiler/)
[![Documentation Status](https://readthedocs.org/projects/eprofiler/badge/?version=latest)](https://eprofiler.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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
Ideal for production logs where you need to know if a function finished, how long it took, and why it failed. 
Optinally which args used.

```python
from eprofiler import audit

@audit(label="PAYMENT_GATEWAY", include_args=True)
def process_payment(user_id, amount):
    # Logic here...
    return True

process_payment(123, 50.0)
```
**Output (Standard Logging):**
`INFO: {'timestamp': '2026-03-02T10:00:00.123', 'function': 'process_payment', 'label': 'PAYMENT_GATEWAY', 'args': (123, 50.0), 'status': 'SUCCESS', 'elapsed_seconds': '0.045200'}`

### 2. Basic Timing (`@timeit`)
For quick performance checks during development. By default, results are printed to the console.

```python
from eprofiler import timeit

@timeit(label="Computation")
def my_func():
    return sum(i**2 for i in range(100000))

my_func()
```
**Output:** `{'label': 'Computation', 'function': 'my_func', 'duration': 0.008421}`

### 3. Comprehensive Profiling (`@profile`)
Track time and memory (current and peak) simultaneously.
```python
from eprofiler import profile

@profile(label="Heavy Task")
def memory_intensive():
    return [x for x in range(1000000)]

memory_intensive()
```
**Output:** `{'label': 'Heavy Task', 'function': 'memory_intensive', 'duration': 0.041200, 'peak': 324502, 'current': 1204}`

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

### Why eprofiler?
1. **Fixed-Width Timing:** All durations use `:.6f` formatting for perfect vertical alignment in logs.
2. **Machine Readable:** All outputs are valid Python dictionaries (easily convertible to JSON).
3. **Fail-Safe:** The `@audit` decorator uses `logger.exception` to ensure stack traces are preserved on failure.
4. **Accuracy Note:** When using `@profile` or `@memit`, Python's `tracemalloc` adds a slight overhead. For the most precise timing-only results, use `@timeit`.