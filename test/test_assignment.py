from textwrap import dedent
import unittest

from test_util import test_pylox, test_error

class TestAssignment(unittest.TestCase):
    def test_associativity(self):
        expected = dedent("""\
            c
            c
            c
            """)
        test_pylox(self, 'assignment/associativity.lox', expected)

    def test_global(self):
        expected = dedent("""\
            before
            after
            arg
            arg
            """)

        test_pylox(self, 'assignment/global.lox', expected)

    def test_grouping(self):
        expected = dedent("""\
            [line 2] Error at '=': Invalid assignment target.
            """)

        test_error(self, 'assignment/grouping.lox', expected, 65)

    def test_infix_operator(self):
        expected = dedent("""\
            [line 3] Error at '=': Invalid assignment target.
            """)

        test_error(self, 'assignment/infix_operator.lox', expected, 65)

    def test_local(self):
        expected = dedent("""\
            before
            after
            arg
            arg
            """)

        test_pylox(self, 'assignment/local.lox', expected)

    def test_prefix_operator(self):
        expected = dedent("""\
            [line 2] Error at '=': Invalid assignment target.
            """)

        test_error(self, 'assignment/prefix_operator.lox', expected, 65)

    def test_syntax(self):
        expected = dedent("""\
            var
            var
            """)

        test_pylox(self, 'assignment/syntax.lox', expected)

    def test_to_this(self):
        expected = dedent("""\
            [line 3] Error at '=': Invalid assignment target.
            """)

        test_error(self, 'assignment/to_this.lox', expected, 65)

    def test_undefined(self):
        expected = dedent("""\
            [line 1] Undefined variable 'unknown'.
            """)

        test_error(self, 'assignment/undefined.lox', expected, 70)
