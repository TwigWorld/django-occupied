from django.db import models, transaction, IntegrityError

from .exceptions import LockAlreadyAcquired


class SimpleLock(models.Model):
    """
    A simple lock record which either exists or doesn't.
    """

    key = models.CharField(
        max_length=255,
        primary_key=True
    )
    acquired = models.DateTimeField(auto_now_add=True)

    @classmethod
    def acquire(cls, key):
        try:
            with transaction.atomic():
                return cls.objects.create(key=key)
        except IntegrityError:
            raise LockAlreadyAcquired(
                "Lock with key '{key}' has already been acquired.".format(
                    key=key
                )
            )

    def release(self):
        self.delete()
