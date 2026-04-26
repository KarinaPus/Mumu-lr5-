"""Decorators used by the application."""

from functools import wraps
from time import perf_counter


def log_execution_time(func):
    """Measure the execution time of a business function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        elapsed_time = perf_counter() - start_time
        return result, elapsed_time

    return wrapper
