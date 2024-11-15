# Process Synchronization Assignment - Solution

## Objective

They idea of our project is to simulate a shared office environment where five users (P1 to P5) require access to shared resources: a printer and a scanner. Each user needs to perform 10 jobs, which include both print and scan tasks. Jobs have varying lengths based on the number of pages:

## Part 1. Job Generator

We created a Job Generator that randomly creates 10 jobs for each of the five users (P1 to P5). Each job is randomly assigned as either a print or scan job and has a random length (short, medium, or large). We simulate random arrival times for each job, where the next job for each user arrives after a random interval (e.g., between 1 to 5 seconds).

## Part 2. Task Implementation

### Task 1: Without Synchronization

We implemented job execution for the generated job queue without using any synchronization mechanisms. We allowed users to access the printer and scanner simultaneously, potentially.

The idea of this method is to show the problems that can occur when multiple users try to access shared resources without any synchronization mechanisms.

### Code

```python
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
```

### Output

```
[1731606016.3064065] P1 (Scan): Page 0/4 at Arrival Time 3 (No Sync) - Job Start
[1731606017.3068378] P1 (Scan): Page 1/4 at Arrival Time 3 (No Sync) | Total Processed Pages: 1
[1731606018.3072708] P1 (Scan): Page 2/4 at Arrival Time 3 (No Sync) | Total Processed Pages: 2
[1731606019.3072076] P2 (Print): Page 0/4 at Arrival Time 4 (No Sync) - Job Start
[1731606019.3077033] P1 (Scan): Page 3/4 at Arrival Time 3 (No Sync) | Total Processed Pages: 3
[1731606020.3076403] P2 (Print): Page 1/4 at Arrival Time 4 (No Sync) | Total Processed Pages: 4
[1731606020.3081362] P1 (Scan): Page 4/4 at Arrival Time 3 (No Sync) | Total Processed Pages: 5
[1731606020.3081362] P1 (Scan): Page 4/4 at Arrival Time 3 (No Sync) - Job Completed

```

Reviewing the output, we can see that the jobs are being processed concurrently without any synchronization. This is due to several issues:

### Deadlocks

Deadlocks can occur when multiple jobs are waiting for resources held by others indefinitely. In this case, if one job is using the printer, another job cannot access the printer until the first job completes. This can lead to a deadlock situation where both jobs are waiting for each other to release

### Race Conditions

Race Conditions can occur when multiple users access the same resource simultaneously, leading to incorrect outputs or mixed results. In this case, multiple jobs are trying to access the printer and scanner at the same time, resulting in mixed outputs and potential errors.

### Task 2: With Synchronization

In the synchronized version, if a previous job has not completed printing or scanning, another job cannot be allowed to run in between due to ```resource_lock```. This means once a job has occupied a resource, it will only be used by the same job until its completion.

### Code
    
```python
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
```

### Output
```
1731680227.981762] P3 (Scan): Page 2/5 at Arrival Time 1 (Sync) | Total Processed Pages: 6
[1731680228.9821935] P3 (Scan): Page 3/5 at Arrival Time 1 (Sync) | Total Processed Pages: 7
[1731680229.9826224] P3 (Scan): Page 4/5 at Arrival Time 1 (Sync) | Total Processed Pages: 8
[1731680230.9830532] P3 (Scan): Page 5/5 at Arrival Time 1 (Sync) | Total Processed Pages: 9
[1731680230.9830532] P3 (Scan): Page 5/5 at Arrival Time 1 (Sync) - Job Completed
[1731680231.983483] P4 (Print): Page 1/2 at Arrival Time 2 (Sync) | Total Processed Pages: 10
[1731680232.988378] P4 (Print): Page 2/2 at Arrival Time 2 (Sync) | Total Processed Pages: 11
[1731680232.988378] P4 (Print): Page 2/2 at Arrival Time 2 (Sync) - Job Completed
```

By looking at this output, we can see that the jobs are being processed sequentially due to the synchronization mechanism. This ensures that only one job can access the printer or scanner at a time, preventing race conditions and deadlocks.

## Mutex Syncronization

Mutex synchronization is a method to ensure exclusive access to shared resources. In this case, we use mutexes to ensure that only one job can access the printer or scanner at a time.

### Code

```python
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
```

### Output

```
[1731680285.0360494] P2 (Print): Page 2/3 at Arrival Time 3 (Mutex Sync) | Total Processed Pages: 15
[1731680285.0360494] P3 (Scan): Page 3/5 at Arrival Time 1 (Mutex Sync) | Total Processed Pages: 16
[1731680286.0364795] P3 (Scan): Page 4/5 at Arrival Time 1 (Mutex Sync) | Total Processed Pages: 17
[1731680286.0364795] P2 (Print): Page 3/3 at Arrival Time 3 (Mutex Sync) | Total Processed Pages: 18
[1731680287.03691] P3 (Scan): Page 5/5 at Arrival Time 1 (Mutex Sync) | Total Processed Pages: 19
[1731680288.0373404] P4 (Scan): Page 1/2 at Arrival Time 2 (Mutex Sync) | Total Processed Pages: 20
[1731680289.0362825] P4 (Print): Page 1/2 at Arrival Time 2 (Mutex Sync) | Total Processed Pages: 21
[1731680289.0377707] P4 (Scan): Page 2/2 at Arrival Time 2 (Mutex Sync) | Total Processed Pages: 22
[1731680290.036713] P4 (Print): Page 2/2 at Arrival Time 2 (Mutex Sync) | Total Processed Pages: 23
[1731680291.036647] P5 (Scan): Page 1/4 at Arrival Time 3 (Mutex Sync) | Total Processed Pages: 24
[1731680292.0370777] P5 (Scan): Page 2/4 at Arrival Time 3 (Mutex Sync) | Total Processed Pages: 25
```

