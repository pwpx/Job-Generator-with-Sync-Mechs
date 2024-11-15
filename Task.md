# Process Synchronization Assignment - Task

## Objective
The purpose of this assignment is to help you understand and implement process synchronization mechanisms to prevent race conditions, deadlocks, and incorrect outputs when multiple users attempt to access shared resources (printer and scanner). You will begin by implementing a job generator that creates print and scan jobs at random times for each user, followed by two versions of job execution (one without synchronization and one with synchronization).

## Scenario Description
In a shared office environment, there are five users (P1 to P5), each requiring access to shared resources:
1. **Printer**
2. **Scanner**

Each user needs to perform 10 jobs, which include both print and scan tasks. Jobs have varying lengths based on the number of pages:
- **Short Job**: 1-5 pages
- **Medium Job**: 6-15 pages
- **Large Job**: 16-50 pages

Each page takes 1 second to process. Jobs are pre-emptive, allowing them to be switched mid-process after a page is completed with a time slice of 2 seconds. No other job can interrupt a job mid-page, but once a page completes, another job can be scheduled if necessary. Assume that the longest waiting job first scheduler will be implemented for each resource.

## Assignment Structure

### Part 1: Job Generator

1. **Job Creation**:
   - Write a job generator that randomly creates 10 jobs for each of the five users (P1 to P5).
   - Each job should be randomly assigned as either a print or scan job and should have a random length (short, medium, or large).
   
2. **Random Arrival Times**:
   - The jobs for each user should be generated at random times.
   - Simulate random arrival times for each job, where the next job for each user arrives after a random interval (e.g., between 1 to 5 seconds).
   
3. **Job Output Format**:
   - Each job should have the following details:
     - **User**: Which user created the job (P1 to P5).
     - **Job Type**: Print or scan.
     - **Length**: Number of pages (short, medium, or large).
     - **Arrival Time**: The time when the job is generated (or intended to start).

4. **Log Job Queue**:
   - Store all generated jobs in a job queue or a log, displaying the details of each job.

**Example Job Queue Output**:
```
User P1: Print Job, 5 pages, Arrival Time: 3 seconds
User P2: Scan Job, 12 pages, Arrival Time: 5 seconds
User P3: Print Job, 3 pages, Arrival Time: 7 seconds
...
```

### Part 2: Task Implementation

After generating the jobs, students will implement two versions of the process execution: one without synchronization and one with synchronization.

#### Task 1: Without Synchronization

1. **Job Execution**:
   - Implement job execution for the generated job queue without using any synchronization mechanisms.
   - Allow users to access the printer and scanner simultaneously, potentially resulting in race conditions and mixed outputs.

2. **Execution Constraints**:
   - Each job can be pre-empted after a page is printed or scanned, allowing another job to be scheduled.
   - However, no job should interrupt another mid-page.

3. **Expected Issues**:
   - **Race Conditions**: Multiple users may access the same resource simultaneously, leading to incorrect outputs or mixed results.
   - **Deadlocks**: Potential for deadlock if multiple jobs wait for resources held by others indefinitely.

4. **Output Format**:
   - Log each job’s progress, showing page-by-page status, including any potential errors or inconsistencies caused by concurrent access.

#### Task 2: With Synchronization

In the synchronized version, if a previous job has not completed printing or scanning, another job cannot be allowed to run in between, meaning once a job has occupied a resource, it will only be used by the same job until its completion.

1. **Implement Synchronization Mechanisms in three separate codes**:
   - Apply synchronization to prevent race conditions and deadlocks:
     - Use **mutexes** to ensure exclusive access to the printer and scanner.
     - Use **semaphores** to control job switching and prioritize or queue jobs.
     - Implement **Peterson’s Solution** on one of the resources (e.g., printer) to demonstrate another way to achieve mutual exclusion.

2. **Job Execution**:
   - Ensure each user’s job can access the resources without interfering with other jobs.
   - Jobs should be allowed to switch only after a page is completed or when the job itself is complete.

3. **Pre-emptive Scheduling with Synchronization**:
   - Allow job switching only at page boundaries.
   - Ensure no two jobs run on the same resource simultaneously, preventing race conditions.

4. **Comparative Analysis of Synchronization Mechanisms**:
   - **Mutexes**: Used for exclusive access to resources, preventing data inconsistencies.
   - **Semaphores**: Manage multiple job requests in a controlled way, ensuring proper prioritization.
   - **Peterson’s Solution**: Allows mutual exclusion for two processes at a time, demonstrating another approach to prevent interference.

5. **Performance and Accuracy**:
   - Record completion times for each job and compare the performance and accuracy of each synchronization mechanism.

6. **Output Format**:
   - Log each job’s status, showing which job and page is currently in progress, when it’s pre-empted, and when it’s complete.

## Deliverables
A single zipped folder containing the following items:
1. **Source Code**:
   - Submit the source code for the job generator and both task implementations (without synchronization and with synchronization).
   - Ensure each part of the code is well-documented.
2. **Report**:
   - **Job Generator**: Describe how jobs are generated and how random times are simulated.
   - **Without Synchronization**: Document observed issues such as race conditions and deadlocks.
   - **With Synchronization**: Explain the implementation of each synchronization mechanism and how it prevents race conditions and deadlocks.
   - **Comparative Analysis**: Compare the performance and accuracy of mutexes, semaphores, and Peterson’s solution.
3. **Testing and Results**:
   - Run each version multiple times to observe consistency.
   - Include output samples showing both the unsynchronized and synchronized versions.
   - Record page-by-page status for each job, indicating when a job is pre-empted or switched.
