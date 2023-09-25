import functools
import time
from collections.abc import Callable
from typing import Any

try:
    from django.db import connection, reset_queries
except ModuleNotFoundError:
    pass


def query_debugger(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            reset_queries()
        except NameError:
            raise ModuleNotFoundError("Django framework wasn't installed.")

        start_queries = len(connection.queries)

        start_time = time.perf_counter()
        func(*args, **kwargs)

        end_queries = len(connection.queries)

        print(f"View (function name): {func.__name__}")
        print(f"Queries quantity: {end_queries - start_queries}")
        print(f"Execution time: {(time.perf_counter() - start_time):.3f}s")
    return wrapper
