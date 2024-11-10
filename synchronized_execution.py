import threading
from models import Job
from synchronization_utils import printer_lock, scanner_lock, switching_semaphore
from logger import log_job_progress
import time

def synchronized_print_job(job):
    with printer_lock:
        for page in range(job.pages):
            time.sleep(1)
            log_job_progress(job.user, f"Printing page {page + 1}/{job.pages} with sync.")

def synchronized_scan_job(job):
    with scanner_lock:
        for page in range(job.pages):
            time.sleep(1)
            log_job_progress(job.user, f"Scanning page {page + 1}/{job.pages} with sync.")

def run_jobs_synchronized(jobs):
    threads = []
    for job in jobs:
        if job.job_type == 'Print':
            t = threading.Thread(target=synchronized_print_job, args=(job,))
        else:
            t = threading.Thread(target=synchronized_scan_job, args=(job,))
        threads.append(t)
        t.start()
        time.sleep(job.arrival_time)

    for t in threads:
        t.join()
