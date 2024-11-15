﻿import random
from models import Job

def generate_small_job_queue():
    users = ['P1', 'P2', 'P3', 'P4', 'P5']
    job_types = ['Print', 'Scan']
    job_queue = []
    for user in users:
        arrival_time = 0
        for _ in range(10):
            job_type = random.choice(job_types)
            if random.random() < 0.33:
                pages = random.randint(1, 5)
            elif random.random() < 0.5:
                pages = random.randint(6, 15)
            else:
                pages = random.randint(16, 50)
            arrival_time += random.randint(1, 5)
            job_queue.append(Job(user, job_type, pages, arrival_time))
    job_queue.sort(key=lambda job: job.arrival_time)
    return job_queue