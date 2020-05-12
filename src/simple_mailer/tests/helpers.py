import os
from functools import wraps
from typing import Callable


def with_environ_var(key, value) -> Callable:
    """Define a temporary environment variable for the test"""

    def _outer(test_func) -> Callable:
        """Decorate a test function"""

        @wraps(test_func)
        def _inner(*args, **kwargs) -> None:
            """Run the decorated function using the given parameters"""
            try:
                os.environ.setdefault(key, value)
                test_func(*args, **kwargs)
            finally:
                os.environ.pop(key, None)

        return _inner

    return _outer
