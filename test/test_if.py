from textwrap import dedent
import unittest

from test_util import test_pylox, test_error

class TestIf(unittest.TestCase):
    def test_class_in_else(self):
        expected = dedent("""\
            [line 2] Error at 'class': Expect expression.
            """)
        test_error(self, 'if/class_in_else.lox', expected, 65)

    def test_class_in_then(self):
        expected = dedent("""\
            [line 2] Error at 'class': Expect expression.
            """)
        test_error(self, 'if/class_in_then.lox', expected, 65)

    def test_dangling_else(self):
        expected = dedent("""\
            good
            """)
        test_pylox(self, 'if/dangling_else.lox', expected)

    def test_else(self):
        expected = dedent("""\
            good
            good
            block
            """)
        test_pylox(self, 'if/else.lox', expected)

    def test_fun_in_else(self):
        expected = dedent("""\
            [line 2] Error at 'fun': Expect expression.
            """)
        test_error(self, 'if/fun_in_else.lox', expected, 65)

    def test_fun_in_then(self):
        expected = dedent("""\
            [line 2] Error at 'fun': Expect expression.
            """)
        test_error(self, 'if/fun_in_then.lox', expected, 65)

    def test_if(self):
        expected = dedent("""\
            good
            block
            true
            """)
        test_pylox(self, 'if/if.lox', expected)

    def test_truth(self):
        expected = dedent("""\
            false
            nil
            true
            0
            empty
            """)
        test_pylox(self, 'if/truth.lox', expected)

    def test_var_in_else(self):
        expected = dedent("""\
            [line 2] Error at 'var': Expect expression.
            """)
        test_error(self, 'if/var_in_else.lox', expected, 65)

    def test_var_in_then(self):
        expected = dedent("""\
            [line 2] Error at 'var': Expect expression.
            """)
        test_error(self, 'if/var_in_then.lox', expected, 65)
