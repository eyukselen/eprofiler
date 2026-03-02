Usage Guide
===========

`eprofiler` provides a tiered approach to performance measurement, allowing you to choose the level of detail you need—from lightweight timing to deep-dive CPU and memory forensics.

.. note::
   All decorators in `eprofiler` are "smart." You can use them without parentheses for default settings, or with parentheses to provide custom labels and callbacks.

Basic Timing (`@timeit`)
------------------------

Use the `@timeit` decorator for high-performance wall-clock timing.

.. code-block:: python

    from eprofiler import timeit

    # Default usage
    @timeit
    def simple_task():
        pass

    # Custom usage
    @timeit(label="Heavy Computation")
    def heavy_task():
        return [x**2 for x in range(10000)]



Full Health Check (`@profile`)
------------------------------

The `@profile` decorator provides a comprehensive overview of wall-clock duration, CPU time (process time), and memory usage (current and peak).

.. code-block:: python

    from eprofiler import profile

    @profile(label="System Audit")
    def audit_function():
        data = [i for i in range(1000000)]
        return sum(data)

    # Output: {'label': 'System Audit', 'duration': 0.12, 'cpu_time': 0.11, 'peak': 32000, ...}

CPU Forensic Profiling (`@profile_cpu`)
---------------------------------------

When you need to understand how much of the "Wall Time" was actually spent using the processor versus waiting for I/O or sleep, use `@profile_cpu`.

On Unix systems, this also provides a breakdown of **User** vs **System** time and calculates **Efficiency**.

.. code-block:: python

    from eprofiler import profile_cpu

    @profile_cpu(label="I/O vs CPU Test")
    def io_bound_task():
        import time
        time.sleep(1) # This increases 'duration' but not 'cpu_time'
        return sum(range(1000000))



Memory Tracking (`@memit`)
--------------------------

If you are only concerned about memory leaks or peak allocation, use `@memit`. It starts a `tracemalloc` session specifically for that function.

.. code-block:: python

    from eprofiler import memit

    @memit
    def allocate_memory():
        return [0] * (10**6)

The Timer Class
---------------

The `Timer` class is a versatile tool that works as both a decorator and a context manager.

**As a Context Manager:**
Perfect for timing a specific subset of code within a large function.

.. code-block:: python

    from eprofiler import Timer

    def complex_workflow():
        setup_logic()

        with Timer("Database Push") as t:
            # Only this block is timed
            push_to_db()

        print(f"DB Push took: {t.stats['duration']}s")
        teardown_logic()

Callbacks
---------

Instead of printing to `stdout`, you can redirect results to a logger, database, or monitoring service using the `callback` argument.

.. code-block:: python

    import logging

    def log_stats(stats):
        logging.info(f"{stats['function']} ran in {stats['duration']}s")

    @profile(callback=log_stats)
    def production_service():
        pass

Using the Auditor
-----------------

To monitor function inputs and outputs:

.. code-block:: python

   from eprofiler import audit

   @audit()
   def my_function(a, b):
       return a + b