import time


def time_func(func):
    """
    A decorator that prints the time a function takes to execute.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        elapsed_time = end_time - start_time

        print(f"Function '{func.__name__}' took {elapsed_time:.4f} seconds to execute.")

        return result
    return wrapper
