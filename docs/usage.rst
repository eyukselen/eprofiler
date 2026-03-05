Usage Guide
===========

`eprofiler` provides a tiered approach to performance measurement, allowing you to choose the level of detail you need—from lightweight timing to deep-dive CPU and memory forensics.

.. note::
   **The "Smart" Decorator Pattern:** All decorators in `eprofiler` are designed to be intuitive. You can use them in two ways:

   1. **Simple:** `@profile` (no parentheses, uses default settings)
   2. **Configured:** `@profile(label="API", callback=my_func)` (with parentheses for custom options)

Basic Timing (`@timeit`)
------------------------

Use the `@timeit` decorator for high-performance wall-clock timing with minimal overhead.

.. code-block:: python

    from eprofiler import timeit

    # Simple usage
    @timeit
    def simple_task():
        pass

    # Custom label
    @timeit(label="Heavy Computation")
    def heavy_task():
        return [x**2 for x in range(10000)]

Full Health Check (`@profile`)
------------------------------

The `@profile` decorator is your "all-in-one" tool. It measures wall-clock duration, CPU time, and memory usage (current and peak) in a single pass.

.. code-block:: python

    from eprofiler import profile

    @profile(label="System Audit")
    def audit_function():
        data = [i for i in range(1000000)]
        return sum(data)

    # The result is a dictionary-like object containing:
    # {'label': 'System Audit', 'duration': 0.12, 'cpu_time': 0.11, 'peak_mb': 32.4, ...}

CPU Forensic Profiling (`@profile_cpu`)
---------------------------------------

When you need to understand how much of the "Wall Time" was actually spent using the processor versus waiting for I/O or sleep, use `@profile_cpu`.

On Unix-like systems, this provides a breakdown of **User** vs **System** time and calculates **Efficiency** ($Efficiency = \frac{CPU\ Time}{Duration} \times 100$).

.. code-block:: python

    from eprofiler import profile_cpu

    @profile_cpu(label="I/O vs CPU Test")
    def io_bound_task():
        import time
        time.sleep(1) # This increases 'duration' but not 'cpu_time'
        return sum(range(1000000))

Memory Tracking (`@memit`)
--------------------------

If you are only concerned about memory leaks or peak allocation, use `@memit`. It uses Python's `tracemalloc` to provide high-precision memory delta tracking.

.. code-block:: python

    from eprofiler import memit

    @memit
    def allocate_memory():
        return [0] * (10**6)

The Timer Class (and Context Manager)
-------------------------------------

The `Timer` class is the engine behind `@timeit`. It is particularly useful as a **Context Manager** for timing specific blocks of code inside a larger function.

.. code-block:: python

    from eprofiler import Timer

    def complex_workflow():
        setup_logic()

        with Timer("Database Push") as t:
            # Only this block is timed
            push_to_db()

        print(f"DB Push took: {t.duration}s")
        teardown_logic()

Callbacks and Redirection
-------------------------

By default, `eprofiler` prints results to `stdout`. You can redirect results to a logger, a file, or a monitoring service by passing a `callback` function.

.. code-block:: python

    import logging

    def log_stats(stats):
        # 'stats' is a dictionary containing all measured metrics
        logging.info(f"{stats['function']} ran in {stats['duration']}s")

    @profile(callback=log_stats)
    def production_service():
        pass

Using the Auditor (`@audit`)
----------------------------

To monitor function inputs and outputs for debugging data-processing pipelines:

.. code-block:: python

   from eprofiler import audit

   @audit()
   def process_data(user_id, mode="fast"):
       return {"status": "ok"}