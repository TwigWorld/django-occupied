from django.test import TransactionTestCase

from ..decorators import do_or_fail, do_or_die
from ..exceptions import LockAlreadyAcquired
from ..models import SimpleLock


# These tests rely on 'clashing' functions being run at the same time. Ideally
# this would be done using threading, but the setup of Django test DB (Django 1.7)
# means that threads don't share the same database.


class TestDecorators(TransactionTestCase):

    def test_no_clash(self):
        """Functions with different names -- no clash"""

        @do_or_fail
        def test_function_1():
            @do_or_die
            def test_function_2():
                return "test_function_2"

            inner_value = test_function_2()
            return "test_function_1", inner_value

        self.assertEquals(test_function_1(), ("test_function_1", "test_function_2"))

    def test_clash_no_error(self):
        """Functions with same names -- clash (return None)"""

        @do_or_fail
        def test_function():
            @do_or_die
            def test_function():  # Same name, so will clash
                return "test_function"

            inner_value = test_function()
            return "test_function", inner_value

        self.assertEquals(test_function(), ("test_function", None))

    def test_clash_error(self):
        """Functions with same names -- clash (raise exception)"""

        @do_or_fail
        def test_function():
            @do_or_fail
            def test_function():
                return "test_function"

            inner_value = test_function()
            return "test_function", inner_value

        with self.assertRaises(LockAlreadyAcquired):
            test_function()

    def test_clash_shared_name_no_error(self):
        """Functions with shared names -- clash (return None)"""

        @do_or_fail("shared_name")
        def test_function_1():
            @do_or_die("shared_name")
            def test_function_2():
                return "test_function_2"

            inner_value = test_function_2()
            return "test_function_1", inner_value

        self.assertEquals(test_function_1(), ("test_function_1", None))

    def test_clash_shared_name_error(self):
        """Functions with shared names -- clash (raise Exception)"""

        @do_or_fail("shared_name")
        def test_function_1():
            @do_or_fail("shared_name")
            def test_function_2():
                return "test_function_2"

            inner_value = test_function_2()
            return "test_function_1", inner_value

        with self.assertRaises(LockAlreadyAcquired):
            test_function_1()

    def test_key_created_and_cleared(self):
        @do_or_fail("test_function")
        def test_function(unittest):
            unittest.assertEquals(
                SimpleLock.objects.filter(key="test_function").count(), 1
            )

        test_function(self)
        self.assertEquals(SimpleLock.objects.filter(key="test_function").count(), 0)

    def test_exception_clears_key(self):
        @do_or_fail("failure_function")
        def test_function_1():
            raise AttributeError

        with self.assertRaises(AttributeError):
            test_function_1()
        self.assertEqual(SimpleLock.objects.filter(key="failure_function").count(), 0)
