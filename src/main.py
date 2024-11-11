from job_generator import generate_small_job_queue
from unsynchronized_execution import run_jobs_unsynchronized
from synchronized_execution import run_jobs_mutex, run_jobs_semaphore, run_jobs_peterson
from logger import initialize_logger, display_log

if __name__ == "__main__":
    initialize_logger()

    # Generate a small job queue for testing
    job_queue = generate_small_job_queue()

    # Test unsynchronized execution
    print("\n--- Running without Synchronization ---")
    run_jobs_unsynchronized(job_queue)
    display_log()

    # Test mutex-based synchronization
    initialize_logger()
    print("\n--- Running with Mutex Synchronization ---")
    run_jobs_mutex(job_queue)
    display_log()

    # Test semaphore-based synchronization
    initialize_logger()
    print("\n--- Running with Semaphore Synchronization ---")
    run_jobs_semaphore(job_queue)
    display_log()

    # Test Peterson's solution-based synchronization
    initialize_logger()
    print("\n--- Running with Peterson's Solution Synchronization ---")
    run_jobs_peterson(job_queue)
    display_log()
