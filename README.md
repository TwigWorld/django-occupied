# django-occupied
Adds DB-locks to executables.

Used primarily as a decorator. Whenever a function is run, it attempts to acquire a lock in the DB which is unique to that function. When the function completes or errors, the lock is released and the same function may be run again.

## Installation

Add 'occupied' to your INSTALLED_APPS in settings.

## Usage

The easiest way to use the app is through the decorators. There are two of them:

- do_or_fail
- do_or_die

The former attempts to run the function, and raises LockAlreadyAcquired if the function is already running.

The latter attempts to run the function, and simply does nothing if the function is already running. Be careful if you are expecting a return value as this will return None in the event that the function is not executed.

### Simple example

The simple way is to use the decorator without arguments, in which case the function module and name will be used.

```python
@do_or_die
def my_function(*args, **kwargs):
    ...
```

If you want to lock the function against a specific key (whether to avoid clashes on functions with the same name and module, or to make different functions mutually exclusive), pass in an argument to the decorator as follows:

```python
@do_or_fail('someuniquekey')
def my_function(*args, **kwargs):
    ...
```