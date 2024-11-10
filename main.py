from job_generator import generate_jobs
from unsynchronized_execution import run_jobs_unsynchronized
from synchronized_execution import run_jobs_synchronized
from logger import initialize_logger, display_log

if __name__ == "__main__":
    initialize_logger()
    job_queue = generate_jobs()
    print("\n--- Running without Synchronization ---")
    run_jobs_unsynchronized(job_queue)
    display_log()

    print("\n--- Running with Synchronization ---")
    run_jobs_synchronized(job_queue)
    display_log()
