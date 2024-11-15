from job_generator import generate_small_job_queue
from unsynchronized_execution import run_jobs_unsynchronized
from synchronized_execution import run_jobs_mutex, run_jobs_semaphore, run_jobs_peterson, run_jobs_synchronized
from logger import initialize_logger, display_log

if __name__ == "__main__":
    initialize_logger()

    job_queue = generate_small_job_queue()

    print("\n--- Running without Synchronization ---")
    run_jobs_unsynchronized(job_queue)
    display_log()

    print("\n--- Running with Synchronization ---")
    run_jobs_synchronized(job_queue)
    display_log()

    initialize_logger()
    print("\n--- Running with Mutex Synchronization ---")
    run_jobs_mutex(job_queue)
    display_log()

    initialize_logger()
    print("\n--- Running with Semaphore Synchronization ---")
    run_jobs_semaphore(job_queue)
    display_log()

    initialize_logger()
    print("\n--- Running with Peterson's Solution Synchronization ---")
    run_jobs_peterson(job_queue)
    display_log()