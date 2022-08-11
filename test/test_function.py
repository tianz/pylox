from textwrap import dedent
import unittest

from test_util import test_pylox, test_error

class TestFunction(unittest.TestCase):
    def test_body_must_be_block(self):
        expected = dedent("""\
            [line 3] Error at '123': Expect '{' before function body.
            """)
        test_error(self, 'function/body_must_be_block.lox', expected, 65)

    def test_empty_body(self):
        expected = dedent("""\
            nil
            """)
        test_pylox(self, 'function/empty_body.lox', expected)

    def test_extra_arguments(self):
        expected = dedent("""\
            [line 6] Expected 2 arguments but got 4.
            """)
        test_error(self, 'function/extra_arguments.lox', expected, 70)

    def test_local_mutual_recursion(self):
        expected = dedent("""\
            [line 4] Undefined variable 'isOdd'.
            """)
        test_error(self, 'function/local_mutual_recursion.lox', expected, 70)

    def test_local_recursion(self):
        expected = dedent("""\
            21
            """)
        test_pylox(self, 'function/local_recursion.lox', expected)

    def test_missing_arguments(self):
        expected = dedent("""\
            [line 3] Expected 2 arguments but got 1.
            """)
        test_error(self, 'function/missing_arguments.lox', expected, 70)

    def test_missing_comma_in_parameters(self):
        expected = dedent("""\
            [line 3] Error at 'c': Expect ')' after parameters.
            """)
        test_error(self, 'function/missing_comma_in_parameters.lox', expected, 65)

    def test_mutual_recursion(self):
        expected = dedent("""\
            true
            true
            """)
        test_pylox(self, 'function/mutual_recursion.lox', expected)

    def test_nested_call_with_arguments(self):
        expected = dedent("""\
            hello world
            """)
        test_pylox(self, 'function/nested_call_with_arguments.lox', expected)

    def test_parameters(self):
        expected = dedent("""\
            0
            1
            3
            6
            10
            15
            21
            28
            36
            """)
        test_pylox(self, 'function/parameters.lox', expected)

    def test_print(self):
        expected = dedent("""\
            <fn foo>
            <native fn>
            """)
        test_pylox(self, 'function/print.lox', expected)

    def test_too_many_arguments(self):
        expected = dedent("""\
            [line 260] Error at 'a': Can't have more than 255 arguments.
            """)
        test_error(self, 'function/too_many_arguments.lox', expected, 65)

    def test_too_many_parameters(self):
        expected = dedent("""\
            [line 257] Error at 'a': Can't have more than 255 parameters.
            """)
        test_error(self, 'function/too_many_parameters.lox', expected, 65)
