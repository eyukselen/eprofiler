import time
import sys
import os

# to import as if it is a package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from eprofiler import timeit, Timer, memit, profile, profile_cpu


# region profile_cpu
@profile_cpu(label="Heavy Computation")
def compute_pi():
    return sum(1/i**2 for i in range(1, 1000000))

compute_pi()
# endregion

# region timeit default usage
@timeit
def function_for_timeit():
    a = 0
    for x in range(1000):
        a += x


function_for_timeit()

# endregion

# region with label or callback function
def callback_func(stat_dict):
    print(f"{stat_dict}")

@timeit(label="Execution Time with callback", callback=callback_func)
def function_for_timeit_with_callback():
    a = 0
    for x in range(1000):
        a += x

function_for_timeit_with_callback()

# endregion

# region memit

@memit(label="Execution Memory")
def function_for_memit():
    a = 0
    for x in range(1000000):
        a += x

function_for_memit()

# endregion

# region profile
@profile(label="Data Batch")
def process_data():
    return [x for x in range(1000000)]

process_data()
# endregion

# region Timer class
@Timer(label="class decorator")
def function_for_timer_class():
    a = 0
    for x in range(1000):
        a += x


function_for_timer_class()

# endregion

# region Timer class as context manager

def function_for_context_manager():
    a = 0
    for x in range(1000):
        a += x


with Timer(label="context manager") as f:
    function_for_context_manager()

print(f.stats)

# endregion


