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
1731704138.52896] P1 (Scan): Page 5/48 at Arrival Time 1 (No Sync) | Total Processed Pages: 60
[1731704138.5716166] P4 (Print): Page 10/11 at Arrival Time 5 (No Sync) | Total Processed Pages: 61
[1731704138.5716166] P1 (Scan): Page 17/24 at Arrival Time 3 (No Sync) | Total Processed Pages: 62
[1731704139.5283983] P5 (Print): Page 1/8 at Arrival Time 2 (No Sync) | Total Processed Pages: 63
[1731704139.5293903] P1 (Scan): Page 6/48 at Arrival Time 1 (No Sync) | Total Processed Pages: 64
[1731704139.5720463] P4 (Print): Page 11/11 at Arrival Time 5 (No Sync) | Total Processed Pages: 65
[1731704139.5720463] P4 (Print): Page 11/11 at Arrival Time 5 (No Sync) - Job Completed
[1731704139.5720463] P1 (Scan): Page 18/24 at Arrival Time 3 (No Sync) | Total Processed Pages: 66
[1731704140.5283325] P3 (Scan): Page 0/3 at Arrival Time 4 (No Sync) - Job Start

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
[1731704349.0067] P2 (Scan): Page 8/10 at Arrival Time 1 (Sync) | Total Processed Pages: 36
[1731704350.0071309] P2 (Scan): Page 9/10 at Arrival Time 1 (Sync) | Total Processed Pages: 37
[1731704351.0075607] P2 (Scan): Page 10/10 at Arrival Time 1 (Sync) | Total Processed Pages: 38
[1731704351.0075607] P2 (Scan): Page 10/10 at Arrival Time 1 (Sync) - Job Completed
[1731704352.0079908] P5 (Print): Page 1/5 at Arrival Time 1 (Sync) | Total Processed Pages: 39
[1731704353.008421] P5 (Print): Page 2/5 at Arrival Time 1 (Sync) | Total Processed Pages: 40
[1731704354.0088513] P5 (Print): Page 3/5 at Arrival Time 1 (Sync) | Total Processed Pages: 41
[1731704355.0092819] P5 (Print): Page 4/5 at Arrival Time 1 (Sync) | Total Processed Pages: 42
[1731704356.0097125] P5 (Print): Page 5/5 at Arrival Time 1 (Sync) | Total Processed Pages: 43
[1731704356.0097125] P5 (Print): Page 5/5 at Arrival Time 1 (Sync) - Job Completed

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
[1731704993.1866019] P3 (Print): Page 1/2 at Arrival Time 4 (Mutex Sync) | Total Processed Pages: 57
[1731704994.1855438] P1 (Scan): Page 21/24 at Arrival Time 2 (Mutex Sync) | Total Processed Pages: 58
[1731704994.1870332] P3 (Print): Page 2/2 at Arrival Time 4 (Mutex Sync) | Total Processed Pages: 59
[1731704995.1859744] P1 (Scan): Page 22/24 at Arrival Time 2 (Mutex Sync) | Total Processed Pages: 60
[1731704995.1874619] P5 (Print): Page 1/8 at Arrival Time 1 (Mutex Sync) | Total Processed Pages: 61
[1731704996.186404] P1 (Scan): Page 23/24 at Arrival Time 2 (Mutex Sync) | Total Processed Pages: 62
[1731704996.1878922] P5 (Print): Page 2/8 at Arrival Time 1 (Mutex Sync) | Total Processed Pages: 63
[1731704997.1868343] P1 (Scan): Page 24/24 at Arrival Time 2 (Mutex Sync) | Total Processed Pages: 64
[1731704997.1883228] P5 (Print): Page 3/8 at Arrival Time 1 (Mutex Sync) | Total Processed Pages: 65
```

## Semaphore Syncronization

Semaphore synchronization is a method to control job switching and prioritize or queue jobs. In this case, we use semaphores to ensure that only one job can access the printer or scanner at a time.

### Code

```python
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
```

### Output
```
[1731683535.3165627] P2 (Print): Page 3/5 at Arrival Time 2 (Semaphore Sync) | Total Processed Pages: 3
[1731683536.3328676] P2 (Print): Page 4/5 at Arrival Time 2 (Semaphore Sync) | Total Processed Pages: 4
[1731683537.333297] P2 (Print): Page 5/5 at Arrival Time 2 (Semaphore Sync) | Total Processed Pages: 5
[1731683538.3342218] P1 (Print): Page 1/5 at Arrival Time 5 (Semaphore Sync) | Total Processed Pages: 6
[1731683539.334652] P1 (Print): Page 2/5 at Arrival Time 5 (Semaphore Sync) | Total Processed Pages: 7
[1731683540.335082] P1 (Print): Page 3/5 at Arrival Time 5 (Semaphore Sync) | Total Processed Pages: 8
[1731683541.3355126] P1 (Print): Page 4/5 at Arrival Time 5 (Semaphore Sync) | Total Processed Pages: 9
[1731683542.335943] P1 (Print): Page 5/5 at Arrival Time 5 (Semaphore Sync) | Total Processed Pages: 10
[1731683543.3363736] P3 (Scan): Page 1/2 at Arrival Time 5 (Semaphore Sync) | Total Processed Pages: 11
```

### Peterson's Synchronization algorithm

Peterson's algorithm is a classic software-based solution for achieving mutual exclusion between two processes. It ensures that only one process can enter the critical section at a time, preventing race conditions. The algorithm uses two shared variables: ```flag``` and ```turn```.  
### Key Concepts:

* **Flags**: Each process has a flag that indicates whether it wants to enter the critical section.

* **Turn**: A shared variable that indicates whose turn it is to enter the critical section.

### Code

```python
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
```

### Output
```
[1731706039.8708134] P5 (Print): Page 3/9 at Arrival Time 3 (Peterson's Sync) | Total Processed Pages: 73
[1731706039.9179335] P5 (Print): Page 7/8 at Arrival Time 1 (Peterson's Sync) | Total Processed Pages: 74
[1731706040.1956928] P1 (Scan): Page 3/48 at Arrival Time 4 (Peterson's Sync) | Total Processed Pages: 75
[1731706040.8712435] P5 (Print): Page 4/9 at Arrival Time 3 (Peterson's Sync) | Total Processed Pages: 76
[1731706040.9183633] P5 (Print): Page 8/8 at Arrival Time 1 (Peterson's Sync) | Total Processed Pages: 77
[1731706041.196123] P1 (Scan): Page 4/48 at Arrival Time 4 (Peterson's Sync) | Total Processed Pages: 78
[1731706041.871674] P5 (Print): Page 5/9 at Arrival Time 3 (Peterson's Sync) | Total Processed Pages: 79
[1731706042.196553] P1 (Scan): Page 5/48 at Arrival Time 4 (Peterson's Sync) | Total Processed Pages: 80
[1731706042.8721042] P5 (Print): Page 6/9 at Arrival Time 3 (Peterson's Sync) | Total Processed Pages: 81
```

## Conclusion

In this project, we implemented two versions of the process execution: one without synchronization and one with synchronization. We demonstrated the issues that can arise when multiple users try to access shared resources concurrently and showed how synchronization mechanisms can prevent race conditions and deadlocks.