import os
from functools import wraps
from typing import Callable

_unset = object()


def with_environ_var(key, value) -> Callable:
    """Define a temporary environment variable for the test"""

    def _outer(test_func) -> Callable:
        """Decorate a test function"""

        @wraps(test_func)
        def _inner(*args, **kwargs) -> None:
            """Run the decorated function using the given parameters"""
            prev = os.environ.pop(key, _unset)
            try:
                os.environ.setdefault(key, str(value))
                test_func(*args, **kwargs)
            finally:
                os.environ.pop(key, None)
                if prev is not _unset:
                    os.environ.setdefault(key, prev)

        return _inner

    return _outer
