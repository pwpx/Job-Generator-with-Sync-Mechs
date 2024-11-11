# unsynchronized_execution.py

import threading
from models import Job
from logger import log_job_progress
import time
import random


def print_job(job):
    # Simulate printing job without synchronization
    for page in range(1, job.pages + 1):
        time.sleep(1)  # Simulate 1 second per page
        log_job_progress(job.user, "Print", job.pages, page, job.arrival_time, "(No Sync)")


def scan_job(job):
    # Simulate scanning job without synchronization
    for page in range(1, job.pages + 1):
        time.sleep(1)  # Simulate 1 second per page
        log_job_progress(job.user, "Scan", job.pages, page, job.arrival_time, "(No Sync)")


def run_jobs_unsynchronized(jobs):
    threads = []
    for job in jobs:
        # Randomize arrival time between 1 to 5 seconds for each job
        job.arrival_time = random.randint(1, 5)

        # Determine the job type and assign the respective function
        if job.job_type == 'Print':
            t = threading.Thread(target=print_job, args=(job,))
        else:
            t = threading.Thread(target=scan_job, args=(job,))
        threads.append(t)

        # Start the thread and wait for the arrival time to simulate staggered job start
        t.start()
        time.sleep(job.arrival_time)  # Simulate the random arrival time

    # Wait for all threads to complete
    for t in threads:
        t.join()
