import time

log = []

def initialize_logger():
    global log
    log = []

def log_job_progress(user, job_type, pages, current_page, arrival_time, sync_type=""):
    timestamp = time.time()
    log_message = (f"[{timestamp}] {user} ({job_type}): Page {current_page}/{pages} "
                   f"at Arrival Time {arrival_time} {sync_type}")
    log.append(log_message)
    print(log_message)

def display_log():
    print("\nJob Execution Log:")
    for entry in log:
        print(entry)