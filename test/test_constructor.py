from textwrap import dedent
import unittest

from test_util import test_pylox, test_error

class TestConstructor(unittest.TestCase):
    def test_arguments(self):
        expected = dedent("""\
            init
            1
            2
            """)
        test_pylox(self, 'constructor/arguments.lox', expected)

    def test_call_init_early_return(self):
        expected = dedent("""\
            init
            init
            Foo instance
            """)
        test_pylox(self, 'constructor/call_init_early_return.lox', expected)

    def test_call_init_explicitly(self):
        expected = dedent("""\
            Foo.init(one)
            Foo.init(two)
            Foo instance
            init
            """)
        test_pylox(self, 'constructor/call_init_explicitly.lox', expected)

    def test_default(self):
        expected = dedent("""\
            Foo instance
            """)
        test_pylox(self, 'constructor/default.lox', expected)

    def test_default_arguments(self):
        expected = dedent("""\
            [line 3] Expected 0 arguments but got 3.
            """)
        test_error(self, 'constructor/default_arguments.lox', expected, 70)

    def test_early_return(self):
        expected = dedent("""\
            init
            Foo instance
            """)
        test_pylox(self, 'constructor/early_return.lox', expected)

    def test_extra_arguments(self):
        expected = dedent("""\
            [line 8] Expected 2 arguments but got 4.
            """)
        test_error(self, 'constructor/extra_arguments.lox', expected, 70)

    def test_init_not_method(self):
        expected = dedent("""\
            not initializer
            """)
        test_pylox(self, 'constructor/init_not_method.lox', expected)

    def test_missing_arguments(self):
        expected = dedent("""\
            [line 5] Expected 2 arguments but got 1.
            """)
        test_error(self, 'constructor/missing_arguments.lox', expected, 70)

    def test_return_in_nested_function(self):
        expected = dedent("""\
            bar
            Foo instance
            """)
        test_pylox(self, 'constructor/return_in_nested_function.lox', expected)

    def test_return_value(self):
        expected = dedent("""\
            [line 3] Error at 'return': Can't return a value from an initializer.
            """)
        test_error(self, 'constructor/return_value.lox', expected, 65)
