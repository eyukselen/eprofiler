import pytest
import logging
import ast
from eprofiler import audit


def test_audit_success_logic(caplog):
    # 1. Setup: Capture INFO level logs
    caplog.set_level(logging.INFO)

    @audit(label="PERFORMANCE_CHECK")
    def add(a, b):
        return a + b

    # 2. Execution
    result = add(10, 20)

    # 3. Validation
    assert result == 30
    assert len(caplog.records) == 1

    # Parse the actual log string sent to the console
    log_record = caplog.records[0]
    payload = ast.literal_eval(log_record.message)

    assert log_record.levelname == "INFO"
    assert payload["status"] == "SUCCESS"
    assert payload["label"] == "PERFORMANCE_CHECK"

    # Verify our "Predictable Format" (.6f)
    seconds_str = payload["elapsed_seconds"]
    assert isinstance(seconds_str, str)
    assert "." in seconds_str
    # Ensure there are exactly 6 digits after the decimal
    decimal_part = seconds_str.split(".")[1]
    assert len(decimal_part) == 6


def test_audit_failure_logic(caplog):
    caplog.set_level(logging.ERROR)

    @audit()
    def divide_by_zero():
        return 1 / 0

    # Ensure the decorator re-raises the error so the app doesn't swallow it
    with pytest.raises(ZeroDivisionError):
        divide_by_zero()

    # Check that the failure was captured in the logs
    assert len(caplog.records) == 1
    log_record = caplog.records[0]
    payload = ast.literal_eval(log_record.message)

    assert log_record.levelname == "ERROR"
    assert payload["status"] == "FAIL"
    assert payload["error"] == "ZeroDivisionError"
    assert "division by zero" in payload["message"]


def test_audit_callback_no_logging(caplog):
    # If a callback is used, the logger should remain silent
    caplog.set_level(logging.INFO)
    results = []

    @audit(callback=lambda p: results.append(p))
    def do_nothing():
        pass

    do_nothing()

    # Logger should be empty because callback took over
    assert len(caplog.records) == 0
    # Results should contain the raw dictionary
    assert len(results) == 1
    assert results[0]["status"] == "SUCCESS"


def test_audit_complex_args(caplog):
    caplog.set_level(logging.INFO)

    @audit(include_args=True)
    def complex_func(*args, **kwargs):
        return None

    complex_func(1, "test", key="value", nested={"a": 1})

    payload = ast.literal_eval(caplog.records[0].message)

    # Check that positional and keyword arguments are preserved
    assert payload["args"] == (1, "test")
    assert payload["kwargs"] == {"key": "value", "nested": {"a": 1}}