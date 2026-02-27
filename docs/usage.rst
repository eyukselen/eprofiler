Usage Guide
===========

`eprofiler` provides multiple ways to measure performance, from simple timing to detailed memory profiling.

Basic Timing
------------

Use the `@timeit` decorator to measure the execution time of a function. By default, it prints the results to the console.

.. code-block:: python

    from eprofiler import timeit

    @timeit(label="My Task")
    def simple_task():
        return [x**2 for x in range(10000)]

    simple_task()

Capturing Stats in a Dictionary
-------------------------------

If you want to use the profiling data within your application logic, pass a dictionary as the first argument.

.. code-block:: python

    from eprofiler import timeit

    stats = {}

    @timeit(stats, label="Data Processing")
    def process_data():
        # logic here
        pass

    process_data()
    print(f"Total time taken: {stats['duration']}s")

Memory and Full Profiling
-------------------------

To track memory usage (peak and current), use `@memit` or `@profile`. The `@profile` decorator combines both time and memory tracking.

.. code-block:: python

    from eprofiler import profile

    @profile(label="Memory Intensive")
    def heavy_function():
        data = [i for i in range(1000000)]
        return data

    heavy_function()

The Timer Class
---------------

The `Timer` class is highly versatile. It can be used as a decorator or as a context manager to time specific blocks of code.

**As a Context Manager:**

.. code-block:: python

    from eprofiler import Timer

    with Timer("IO Operation") as t:
        # Only this block is timed
        with open("large_file.txt", "w") as f:
            f.write("test" * 1000000)

    print(f"File write took: {t.stats['duration']}s")

**As a Decorator:**

.. code-block:: python

    from eprofiler import Timer

    @Timer(label="Decorated Timer")
    def another_func():
        pass

Using Callbacks
---------------

You can also pass a callback function to handle stats whenever a measurement is completed.

.. code-block:: python

    def my_logger(stats):
        print(f"LOG: {stats['label']} took {stats['duration']}s")

    @timeit(callback=my_logger, label="Callback Example")
    def tracked_func():
        pass