import threading
from models import Job
from logger import log_job_progress
import time
import random

total_processed_pages = 0
total_pages_lock = threading.Lock()

def process_job(job):
    global total_processed_pages
    for page in range(1, job.pages + 1):
        try:
            time.sleep(1)
            with total_pages_lock:
                total_processed_pages += 1
                log_job_progress(job.user, job.job_type, job.pages, page, job.arrival_time, f"(No Sync) | Total Processed Pages: {total_processed_pages}")
        except Exception as e:
            log_job_progress(job.user, job.job_type, job.pages, page, job.arrival_time, f"(No Sync) - Job Interrupted: {str(e)}")

def execute_job(job):
    log_job_progress(job.user, job.job_type, job.pages, 0, job.arrival_time, "(No Sync) - Job Start")
    process_job(job)
    log_job_progress(job.user, job.job_type, job.pages, job.pages, job.arrival_time, "(No Sync) - Job Completed")

def run_jobs_unsynchronized(jobs):
    global total_processed_pages
    total_processed_pages = 0
    threads = []
    for job in jobs:    
        job.arrival_time = random.randint(1, 5)
        t = threading.Thread(target=execute_job, args=(job,))
        threads.append(t)
        t.start()
        time.sleep(job.arrival_time)

    for t in threads:
        t.join()