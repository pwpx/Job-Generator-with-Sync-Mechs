# synchronized_execution.py

import threading
from models import Job
from synchronization_utils import printer_lock, scanner_lock, switching_semaphore, peterson_flags, peterson_turn
from logger import log_job_progress
import time

# Mutex Synchronization Implementation

def mutex_print_job(job):
    with printer_lock:
        for page in range(1, job.pages + 1):
            time.sleep(1)  # Simulate processing time per page
            log_job_progress(job.user, "Print", job.pages, page, job.arrival_time, "(Mutex Sync)")

def mutex_scan_job(job):
    with scanner_lock:
        for page in range(1, job.pages + 1):
            time.sleep(1)
            log_job_progress(job.user, "Scan", job.pages, page, job.arrival_time, "(Mutex Sync)")

def run_jobs_mutex(jobs):
    threads = []
    for job in jobs:
        if job.job_type == 'Print':
            t = threading.Thread(target=mutex_print_job, args=(job,))
        else:
            t = threading.Thread(target=mutex_scan_job, args=(job,))
        threads.append(t)
        t.start()
        time.sleep(job.arrival_time)  # Simulate job arrival

    for t in threads:
        t.join()

# Semaphore Synchronization Implementation

def semaphore_print_job(job):
    switching_semaphore.acquire()  # Wait for resource availability
    for page in range(1, job.pages + 1):
        time.sleep(1)
        log_job_progress(job.user, "Print", job.pages, page, job.arrival_time, "(Semaphore Sync)")
    switching_semaphore.release()  # Release after job completes

def semaphore_scan_job(job):
    switching_semaphore.acquire()
    for page in range(1, job.pages + 1):
        time.sleep(1)
        log_job_progress(job.user, "Scan", job.pages, page, job.arrival_time, "(Semaphore Sync)")
    switching_semaphore.release()

def run_jobs_semaphore(jobs):
    threads = []
    for job in jobs:
        if job.job_type == 'Print':
            t = threading.Thread(target=semaphore_print_job, args=(job,))
        else:
            t = threading.Thread(target=semaphore_scan_job, args=(job,))
        threads.append(t)
        t.start()
        time.sleep(job.arrival_time)  # Simulate job arrival

    for t in threads:
        t.join()

# Peterson’s Solution Synchronization Implementation
# This example uses Peterson's solution for the printer resource only, assuming two jobs are attempting to print.

def peterson_print_job(job, user_id):
    # Set up Peterson’s flags for mutual exclusion
    other_user = 1 - user_id
    peterson_flags[user_id] = True
    peterson_turn[0] = other_user

    # Peterson's Solution Entry Protocol
    while peterson_flags[other_user] and peterson_turn[0] == other_user:
        pass  # Wait until the resource is free

    # Critical Section for Print Job
    for page in range(1, job.pages + 1):
        time.sleep(1)  # Simulate processing time per page
        log_job_progress(job.user, "Print", job.pages, page, job.arrival_time, "(Peterson's Sync)")

    # Exit Protocol
    peterson_flags[user_id] = False  # Allow other user access

def peterson_scan_job(job):
    # Scanning will use a mutex lock here to keep the code structure similar
    with scanner_lock:
        for page in range(1, job.pages + 1):
            time.sleep(1)
            log_job_progress(job.user, "Scan", job.pages, page, job.arrival_time, "(Peterson's Sync)")

def run_jobs_peterson(jobs):
    threads = []
    user_id = 0
    for job in jobs:
        if job.job_type == 'Print':

            t = threading.Thread(target=peterson_print_job, args=(job, user_id))
            user_id = 1 - user_id
        else:

            t = threading.Thread(target=peterson_scan_job, args=(job,))
        threads.append(t)
        t.start()
        time.sleep(job.arrival_time)

    for t in threads:
        t.join()
