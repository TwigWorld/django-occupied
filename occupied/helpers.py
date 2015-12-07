from .exceptions import LockAlreadyAcquired
from .models import SimpleLock


def do_or_fail(key, callable, *args, **kwargs):
    """
    Attempt the acquire the lock, execute a callable and then release it. If
    the key has already been acquired, propagate the exception.
    """
    lock = SimpleLock.acquire(key)
    if lock is not None:
        try:
            return callable(*args, **kwargs)
        finally:
            lock.release()


def do_or_die(key, callable, *args, **kwargs):
    """
    Attempt the acquire the lock, execute a callable and then release it. If
    the key has already been acquired, fail silently.
    """
    try:
        return do_or_fail(key, callable, *args, **kwargs)
    except LockAlreadyAcquired:
        pass
