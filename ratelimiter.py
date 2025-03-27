import time
import threading
from collections import deque


class RateLimiter:
    def __init__(self, max_calls_per_minute=60):
        self.max_calls = max_calls_per_minute
        self.interval = 60  # seconds
        self.calls = deque()
        self.lock = threading.Lock()

    def __call__(self, func):
        def wrapped(*args, **kwargs):
            with self.lock:
                # Clean up old timestamps
                now = time.time()
                while self.calls and now - self.calls[0] > self.interval:
                    self.calls.popleft()

                # Check if we've reached the limit
                if len(self.calls) >= self.max_calls:
                    wait_time = self.interval - (now - self.calls[0])
                    if wait_time > 0:
                        print(f"Rate limit reached. Waiting {wait_time:.2f} seconds...")
                        time.sleep(wait_time)

                # Add current timestamp and execute function
                self.calls.append(time.time())

            return func(*args, **kwargs)

        return wrapped