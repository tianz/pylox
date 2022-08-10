from textwrap import dedent
import unittest

from test_util import test_pylox, test_error

class TestFor(unittest.TestCase):
    def class_in_body(self):
        expected = dedent("""\
            [line 2] Error at 'class': Expect expression.
            """)
        test_error(self, 'for/class_in_body.lox', expected, 65)

    def test_closure_in_body(self):
        expected = dedent("""\
            4
            1
            4
            2
            4
            3
            """)
        test_pylox(self, 'for/closure_in_body.lox', expected)

    def test_fun_in_body(self):
        expected = dedent("""\
            [line 2] Error at 'fun': Expect expression.
            """)
        test_error(self, 'for/fun_in_body.lox', expected, 65)

    def test_return_closure(self):
        expected = dedent("""\
            i
            """)
        test_pylox(self, 'for/return_closure.lox', expected)

    def test_return_inside(self):
        expected = dedent("""\
            i
            """)
        test_pylox(self, 'for/return_inside.lox', expected)

    def test_scope(self):
        expected = dedent("""\
            0
            -1
            after
            0
            """)
        test_pylox(self, 'for/scope.lox', expected)

    def test_statement_condition(self):
        expected = dedent("""\
            [line 3] Error at '{': Expect expression.
            [line 3] Error at ')': Expect ';' after expression.
            """)
        test_error(self, 'for/statement_condition.lox', expected, 65)

    def test_statement_increment(self):
        expected = dedent("""\
            [line 2] Error at '{': Expect expression.
            """)
        test_error(self, 'for/statement_increment.lox', expected, 65)

    def test_statement_initializer(self):
        expected = dedent("""\
            [line 3] Error at '{': Expect expression.
            [line 3] Error at ')': Expect ';' after expression.
            """)
        test_error(self, 'for/statement_initializer.lox', expected, 65)

    def test_syntax(self):
        expected = dedent("""\
            1
            2
            3
            0
            1
            2
            done
            0
            1
            0
            1
            2
            0
            1
            """)
        test_pylox(self, 'for/syntax.lox', expected)

    def test_var_in_body(self):
        expected = dedent("""\
            [line 2] Error at 'var': Expect expression.
            """)
        test_error(self, 'for/var_in_body.lox', expected, 65)
