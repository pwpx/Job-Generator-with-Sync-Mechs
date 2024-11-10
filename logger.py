import time

log = []

def initialize_logger():
    global log
    log = []

def log_job_progress(user, message):
    timestamp = time.time()
    log.append(f"[{timestamp}] {user}: {message}")
    print(f"[{timestamp}] {user}: {message}")  # Print in real-time

def display_log():
    print("\nJob Execution Log:")
    for entry in log:
        print(entry)
