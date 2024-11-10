import threading
from models import Job
from logger import log_job_progress
import time

def print_job(job):
    for page in range(job.pages):
        time.sleep(1)
        log_job_progress(job.user, f"Printing page {page + 1}/{job.pages} without sync.")

def scan_job(job):
    for page in range(job.pages):
        time.sleep(1)
        log_job_progress(job.user, f"Scanning page {page + 1}/{job.pages} without sync.")

def run_jobs_unsynchronized(jobs):
    threads = []
    for job in jobs:
        if job.job_type == 'Print':
            t = threading.Thread(target=print_job, args=(job,))
        else:
            t = threading.Thread(target=scan_job, args=(job,))
        threads.append(t)
        t.start()
        time.sleep(job.arrival_time)  # Delay to simulate arrival time

    for t in threads:
        t.join()
