class Job:
    def __init__(self, user, job_type, pages, arrival_time):
        self.user = user
        self.job_type = job_type
        self.pages = pages
        self.arrival_time = arrival_time

    def __repr__(self):
        return f"{self.user}: {self.job_type} Job, {self.pages} pages, Arrival Time: {self.arrival_time}"
