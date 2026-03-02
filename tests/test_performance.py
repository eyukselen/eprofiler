import unittest
import io
import ast
from contextlib import redirect_stdout
from eprofiler import timeit, memit, Timer, profile, profile_cpu


class TestTimeit(unittest.TestCase):
    def test_default_output(self):
        f = io.StringIO()

        @timeit
        def simple(): pass

        with redirect_stdout(f):
            simple()

        stats = ast.literal_eval(f.getvalue().strip())
        self.assertEqual(stats['label'], "Execution Time")
        self.assertEqual(stats['function'], "simple")
        self.assertIn('duration', stats)

    def test_callback(self):
        captured_stats = None

        def my_callback(stats):
            nonlocal captured_stats
            captured_stats = stats

        @timeit(callback=my_callback)
        def add(a, b): return a + b

        with redirect_stdout(io.StringIO()):
            add(10, 20)

        self.assertIsNotNone(captured_stats)
        self.assertEqual(captured_stats['function'], 'add')


class TestMemit(unittest.TestCase):
    def test_output(self):
        f = io.StringIO()

        @memit(label="MemoryTest")
        def allocate(): return [i for i in range(1000)]

        with redirect_stdout(f):
            allocate()

        stats = ast.literal_eval(f.getvalue().strip())
        self.assertEqual(stats['label'], "MemoryTest")
        self.assertIn('current', stats)
        self.assertIn('peak', stats)


class TestTimer(unittest.TestCase):
    def test_context_manager(self):
        with Timer(label="CM_Test") as t:
            _ = sum(range(100))
        self.assertEqual(t.label, "CM_Test")
        self.assertIsInstance(t.stats['duration'], float)

    def test_decorator_args_handling(self):
        f = io.StringIO()
        my_timer = Timer(label="WithArgs")

        @my_timer
        def power_func(base, exponent=2): return base ** exponent

        with redirect_stdout(f):
            result = power_func(10, exponent=3)

        self.assertEqual(result, 1000)
        stats = ast.literal_eval(f.getvalue().strip())
        self.assertEqual(stats['function'], "power_func")


class TestProfile(unittest.TestCase):
    def test_combined_metrics(self):
        """Verifies updated keys: duration, cpu_time, peak, current."""
        f = io.StringIO()

        @profile(label="FullProfile")
        def combined_task(): return sum(range(1000))

        with redirect_stdout(f):
            combined_task()

        stats = ast.literal_eval(f.getvalue().strip())
        self.assertEqual(stats['label'], "FullProfile")
        # Ensure updated keys exist
        self.assertIn('duration', stats)
        self.assertIn('cpu_time', stats)
        self.assertIn('peak', stats)
        self.assertIn('current', stats)

    def test_no_output_on_fail(self):
        """Verifies that stats are NOT printed if the function crashes."""
        f = io.StringIO()

        @profile(label="ShouldFail")
        def crasher():
            raise ValueError("Boom")

        with self.assertRaises(ValueError):
            with redirect_stdout(f):
                crasher()

        # Verify stdout is empty because print(stats) is skipped in profile
        self.assertEqual(f.getvalue().strip(), "")


class TestProfileCPU(unittest.TestCase):
    def test_cpu_metrics_standardized_keys(self):
        """Verifies keys: user_time, system_time, cpu_time, duration, efficiency."""
        f = io.StringIO()

        @profile_cpu(label="CPUTest")
        def cpu_task(): return sum(range(1000))

        with redirect_stdout(f):
            cpu_task()

        stats = ast.literal_eval(f.getvalue().strip())

        # Checking final standardized keys
        self.assertIn('user_time', stats)
        self.assertIn('system_time', stats)
        self.assertIn('cpu_time', stats)
        self.assertIn('duration', stats)
        self.assertIn('efficiency', stats)

    def test_cpu_efficiency_logic(self):
        captured_stats = None

        def callback(s):
            nonlocal captured_stats
            captured_stats = s

        @profile_cpu(callback=callback)
        def heavy_work():
            # Force some CPU work to ensure efficiency isn't exactly 0
            return sum(range(10 ** 6))

        heavy_work()
        self.assertGreater(captured_stats['efficiency'], 0)
        self.assertLessEqual(captured_stats['efficiency'], 100.1)  # Float precision


class TestIntegrity(unittest.TestCase):
    def test_return_values(self):
        @timeit
        def get_n(): return 42

        @profile
        def get_p(): return "ok"

        with redirect_stdout(io.StringIO()):
            self.assertEqual(get_n(), 42)
            self.assertEqual(get_p(), "ok")


if __name__ == '__main__':
    unittest.main()