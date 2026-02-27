import unittest
import io
import ast
from contextlib import redirect_stdout
from eprofiler import timeit, memit, Timer, profile


class TestTimeit(unittest.TestCase):
    def test_default_output(self):
        """Verifies output when no arguments are passed to the decorator."""
        f = io.StringIO()

        @timeit
        def simple(): pass

        with redirect_stdout(f):
            simple()

        stats = ast.literal_eval(f.getvalue().strip())
        self.assertEqual(stats['label'], "Execution Time")  # Testing the default
        self.assertEqual(stats['function'], "simple")

    def test_custom_label(self):
        f = io.StringIO()

        @timeit(label="Benchmarking")
        def heavy(): pass

        with redirect_stdout(f):
            heavy()
        stats = ast.literal_eval(f.getvalue().strip())
        self.assertEqual(stats['label'], "Benchmarking")

    def test_callback(self):
        """Verifies timeit sends stats to a callback instead of printing."""
        captured_stats = None

        def my_callback(stats):
            nonlocal captured_stats
            captured_stats = stats

        @timeit(callback=my_callback)
        def add(a, b):
            return a + b

        f = io.StringIO()
        with redirect_stdout(f):
            result = add(10, 20)

        # 1. Verify function logic
        self.assertEqual(result, 30)
        # 2. Verify callback was called with correct data
        self.assertIsNotNone(captured_stats)
        self.assertEqual(captured_stats['function'], 'add')
        # 3. Verify NOTHING was printed to stdout
        self.assertEqual(f.getvalue().strip(), "")

class TestMemit(unittest.TestCase):
    def test_output(self):
        """Verifies that memit prints memory stats correctly."""
        f = io.StringIO()

        @memit(label="MemoryTest")
        def allocate():
            return [i for i in range(1000)]

        with redirect_stdout(f):
            allocate()

        stats = ast.literal_eval(f.getvalue().strip())
        self.assertEqual(stats['label'], "MemoryTest")
        self.assertIn('current', stats)
        self.assertIn('peak', stats)

    def test_callback(self):
        """Verifies memit sends stats to a callback instead of printing."""
        captured_stats = None

        def my_callback(stats):
            nonlocal captured_stats
            captured_stats = stats

        @memit(callback=my_callback)
        def allocate():
            return [0] * 100

        f = io.StringIO()
        with redirect_stdout(f):
            allocate()

        self.assertIsNotNone(captured_stats)
        self.assertIn('peak', captured_stats)
        self.assertEqual(f.getvalue().strip(), "")

class TestTimer(unittest.TestCase):
    def test_context_manager(self):
        with Timer(label="CM_Test") as t:
            _ = sum(range(100))
        self.assertEqual(t.label, "CM_Test")
        self.assertIsInstance(t.stats['duration'], float)

    def test_decorator_no_args(self):
        """Triggers the 'if not args and not kwargs' branch."""
        f = io.StringIO()
        my_timer = Timer(label="NoArgs")

        @my_timer
        def task():
            return "ok"

        with redirect_stdout(f):
            result = task()

        self.assertEqual(result, "ok")
        stats = ast.literal_eval(f.getvalue().strip())
        self.assertEqual(stats['function'], "task")

    def test_decorator_with_args_and_kwargs(self):
        """Triggers the 'else' branch in Timer.__call__."""
        f = io.StringIO()
        my_timer = Timer(label="WithArgs")

        @my_timer
        def power_func(base, exponent=2):
            return base ** exponent

        with redirect_stdout(f):
            # Passing positional and keyword args to trigger the 'else' branch
            result = power_func(10, exponent=3)

        self.assertEqual(result, 1000)
        stats = ast.literal_eval(f.getvalue().strip())
        self.assertEqual(stats['label'], "WithArgs")
        self.assertEqual(stats['function'], "power_func")


class TestProfile(unittest.TestCase):
    def test_combined_metrics(self):
        """Verifies that the combined profile decorator prints all metrics."""
        f = io.StringIO()

        @profile(label="FullProfile")
        def combined_task():
            return sum(range(1000))

        with redirect_stdout(f):
            result = combined_task()

        output = f.getvalue().strip()
        stats = ast.literal_eval(output)

        # Verify all keys exist in the combined output
        self.assertEqual(stats['label'], "FullProfile")
        self.assertEqual(stats['function'], "combined_task")
        self.assertIn('time_ms', stats)
        self.assertIn('current', stats)
        self.assertIn('peak', stats)
        self.assertEqual(result, 499500)


class TestIntegrity(unittest.TestCase):
    """Tests that apply to all decorators, like return value preservation."""
    def test_return_values(self):
        @timeit
        def get_n(): return 42
        @memit
        def get_s(): return "hi"

        with redirect_stdout(io.StringIO()):
            self.assertEqual(get_n(), 42)
            self.assertEqual(get_s(), "hi")


if __name__ == '__main__':
    unittest.main()
