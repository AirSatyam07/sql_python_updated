import time

class SessionManager:
    def __init__(self, timeout_seconds=300):
        self.timeout = timeout_seconds
        self.start_time = None
        self.user = None

    def start_session(self, user=None):
        self.start_time = time.time()
        self.user = user  # store logged-in user

    def is_active(self):
        if self.start_time is None:
            return False
        return (time.time() - self.start_time) < self.timeout

    def refresh(self):
        self.start_time = time.time()

    def end_session(self):
        self.start_time = None
        self.user = None  # clear user on logout
