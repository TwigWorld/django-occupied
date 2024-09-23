import types

from . import helpers


def do_or_fail(key_or_func=None):
    if isinstance(key_or_func, types.FunctionType):
        func = key_or_func
        key = "{module}.{name}".format(module=func.__module__, name=func.__name__)
    else:
        func = None
        key = key_or_func

    def decorator(func):
        def func_wrapper(*args, **kwargs):
            return helpers.do_or_fail(key, func, *args, **kwargs)

        return func_wrapper

    if func is not None:
        return decorator(func)

    return decorator


def do_or_die(key_or_func=None):
    if isinstance(key_or_func, types.FunctionType):
        func = key_or_func
        key = "{module}.{name}".format(module=func.__module__, name=func.__name__)
    else:
        func = None
        key = key_or_func

    def decorator(func):
        def func_wrapper(*args, **kwargs):
            return helpers.do_or_die(key, func, *args, **kwargs)

        return func_wrapper

    if func is not None:
        return decorator(func)

    return decorator
