from django.db import IntegrityError


class LockAlreadyAcquired(IntegrityError):
    pass
