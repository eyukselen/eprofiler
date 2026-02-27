# eprofiler

**Execution & Memory Profiler for Python**

A lightweight, zero-dependency toolset to monitor execution time and memory usage. 
eprofiler provides decorators and context managers to help you identify bottlenecks 
with minimal code.

[![PyPI version](https://img.shields.io/pypi/v/eprofiler.svg)](https://pypi.org/project/eprofiler/)

## Installation

`pip install eprofiler`

## Features

* @timeit: High-resolution execution timing.
* @memit: Simple peak memory tracking.
* @profile: Combined time and memory profiling in one shot.
* Timer: A versatile class that works as both a context manager and a decorator.
* Stats Capture: Pass a dictionary to handle results programmatically instead of printing.

---

## Usage

### 1. Basic Timing (@timeit)
By default, decorators print a results dictionary to the console.



```python
from eprofiler import timeit

@timeit(label="Computation")
def my_func():
    return sum(i**2 for i in range(100000))

my_func()
```
 Output: {'label': 'Computation', 'function': 'my_func', 'duration': 0.008...}

### 2. Capturing Results in a Dictionary
If you pass a dictionary as the first argument, eprofiler populates it with the results instead of printing.

```python
from eprofiler import timeit

results = {}

@timeit(results)
def process_data():
    # ... logic ...
    pass

process_data()
print(f"Time taken: {results['duration']} seconds")
```

### 3. Comprehensive Profiling (@profile)
Track both time and memory (current and peak) simultaneously.
```python
from eprofiler import profile

@profile(label="Heavy Task")
def memory_intensive():
    return [x for x in range(1000000)]

memory_intensive()
```
Output: {'label': 'Heavy Task', 'function': 'memory_intensive', 'duration': 0.04, 'peak': 324502, 'current': 1204}

### 4. The Timer Class
The Timer class is perfect for timing specific blocks of code or being used as a persistent profiler.

```python
from eprofiler import Timer

# Use as a context manager
with Timer("Database Query") as t:
    # ... code to time ...
    pass
print(t.stats)

# Use as a decorator
@Timer("Critical Path")
def critical_logic():
    pass
```

---

## Links
* PyPI: https://pypi.org/project/eprofiler/
* GitHub: https://github.com/eyukselen/eprofiler
* readthedocs: https://eprofiler.readthedocs.io/en/latest

---

### Accuracy Note
When using @profile or @memit, Python's tracemalloc is enabled. 
This adds a slight "Tracer Tax" (overhead) to execution time. 
For the most precise timing-only results, use @timeit.