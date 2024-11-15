import threading
from models import Job
from synchronization_utils import printer_lock, scanner_lock, switching_semaphore, peterson_flags, peterson_turn
from logger import log_job_progress
import time
import random

total_processed_pages = 0
total_pages_lock = threading.Lock()
resource_lock = threading.Lock()

def process_job(job):
    global total_processed_pages
    time.sleep(job.arrival_time)
    with resource_lock:
        for page in range(1, job.pages + 1):
            try:
                time.sleep(1)
                with total_pages_lock:
                    total_processed_pages += 1
                    log_job_progress(job.user, job.job_type, job.pages, page, job.arrival_time, f"(Sync) | Total Processed Pages: {total_processed_pages}")
            except Exception as e:
                log_job_progress(job.user, job.job_type, job.pages, page, job.arrival_time, f"(Sync) - Job Interrupted: {str(e)}")

def execute_job(job):
    log_job_progress(job.user, job.job_type, job.pages, 0, job.arrival_time, "(Sync) - Job Start")
    process_job(job)
    log_job_progress(job.user, job.job_type, job.pages, job.pages, job.arrival_time, "(Sync) - Job Completed")

def run_jobs_synchronized(jobs):
    global total_processed_pages
    total_processed_pages = 0
    threads = []
    for job in jobs:
        job.arrival_time = random.randint(1, 5)
        t = threading.Thread(target=execute_job, args=(job,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

def mutex_print_job(job):
    global total_processed_pages
    with printer_lock:
        for page in range(1, job.pages + 1):
            time.sleep(1)
            with total_pages_lock:
                total_processed_pages += 1
                log_job_progress(job.user, "Print", job.pages, page, job.arrival_time, f"(Mutex Sync) | Total Processed Pages: {total_processed_pages}")

def mutex_scan_job(job):
    global total_processed_pages
    with scanner_lock:
        for page in range(1, job.pages + 1):
            time.sleep(1)
            with total_pages_lock:
                total_processed_pages += 1
                log_job_progress(job.user, "Scan", job.pages, page, job.arrival_time, f"(Mutex Sync) | Total Processed Pages: {total_processed_pages}")

def run_jobs_mutex(jobs):
    global total_processed_pages
    total_processed_pages = 0
    threads = []
    for job in jobs:
        if job.job_type == 'Print':
            t = threading.Thread(target=mutex_print_job, args=(job,))
        else:
            t = threading.Thread(target=mutex_scan_job, args=(job,))
        threads.append(t)
        t.start()
        time.sleep(job.arrival_time)

    for t in threads:
        t.join()

def semaphore_print_job(job):
    global total_processed_pages
    switching_semaphore.acquire()
    for page in range(1, job.pages + 1):
        time.sleep(1)
        with total_pages_lock:
            total_processed_pages += 1
            log_job_progress(job.user, "Print", job.pages, page, job.arrival_time, f"(Semaphore Sync) | Total Processed Pages: {total_processed_pages}")
    switching_semaphore.release()

def semaphore_scan_job(job):
    global total_processed_pages
    switching_semaphore.acquire()
    for page in range(1, job.pages + 1):
        time.sleep(1)
        with total_pages_lock:
            total_processed_pages += 1
            log_job_progress(job.user, "Scan", job.pages, page, job.arrival_time, f"(Semaphore Sync) | Total Processed Pages: {total_processed_pages}")
    switching_semaphore.release()

def run_jobs_semaphore(jobs):
    global total_processed_pages
    total_processed_pages = 0
    threads = []
    for job in jobs:
        if job.job_type == 'Print':
            t = threading.Thread(target=semaphore_print_job, args=(job,))
        else:
            t = threading.Thread(target=semaphore_scan_job, args=(job,))
        threads.append(t)
        t.start()
        time.sleep(job.arrival_time)

    for t in threads:
        t.join()

def peterson_print_job(job, user_id):
    global total_processed_pages

    other_user = 1 - user_id
    peterson_flags[user_id] = True
    peterson_turn[0] = other_user

    while peterson_flags[other_user] and peterson_turn[0] == other_user:
        pass

    for page in range(1, job.pages + 1):
        time.sleep(1)
        with total_pages_lock:
            total_processed_pages += 1
            log_job_progress(job.user, "Print", job.pages, page, job.arrival_time, f"(Peterson's Sync) | Total Processed Pages: {total_processed_pages}")

    peterson_flags[user_id] = False

def peterson_scan_job(job):
    global total_processed_pages

    with scanner_lock:
        for page in range(1, job.pages + 1):
            time.sleep(1)
            with total_pages_lock:
                total_processed_pages += 1
                log_job_progress(job.user, "Scan", job.pages, page, job.arrival_time, f"(Peterson's Sync) | Total Processed Pages: {total_processed_pages}")

def run_jobs_peterson(jobs):
    global total_processed_pages
    total_processed_pages = 0
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