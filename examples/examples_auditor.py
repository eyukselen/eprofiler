import logging
import sys
import time

from eprofiler import audit

# Setup: Send logs to stdout so we can see them immediately
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

print("--- 1. Basic Auditing ---")
# Define and call immediately to keep context together
@audit
def add(a, b):
    time.sleep(3)
    return a + b

add(5, 10)
# Output: INFO: AUDIT: {'function': 'add', 'status': 'success', ...}

print("\n--- 2. Auditing with Arguments (Privacy Control) ---")
# By default, we don't log args to keep logs clean and secure.
# Switch 'include_args' to True when you need to see the data.
@audit(include_args=True)
def create_user(username, email):
    return f"User {username} created."

create_user("jdoe", "jane@example.com")
# Output: INFO: AUDIT: {..., 'args': ('jdoe', 'jane@example.com'), ...}

print("\n--- 3. Automatic Error Tracking ---")
# The auditor captures the crash status before letting the error pass through.
@audit
def divide_by_zero():
    return 10 / 0

try:
    divide_by_zero()
except ZeroDivisionError:
    print("Caught the expected error in main script.")
# Output: ERROR: AUDIT FAIL: {'function': 'divide_by_zero', 'status': 'failure', 'error': 'ZeroDivisionError'}

print("\n--- 4. Custom Callbacks (Advanced) ---")
# If you don't want to use standard logging, pass a function to 'callback'.
def my_alert_system(data):
    print(f"ALERT: Function {data['function']} finished with status: {data['status']}")

@audit(callback=my_alert_system)
def secure_action():
    return "Secret stuff done"

secure_action()
# Output: ALERT: Function secure_action finished with status: success