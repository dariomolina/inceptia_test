

class ValidateRequests:

    MAX_INCORRECT_REQUESTS = 3

    def __init__(self, incorrect_requests):
        self.incorrect_requests = incorrect_requests

    def __call__(self, function):
        def wrapper(*args, **kwargs):
            if self.incorrect_requests > self.MAX_INCORRECT_REQUESTS:
                raise Exception(f"Exceeded the maximum number of incorrect requests")
            return function(*args, **kwargs)
        return wrapper
