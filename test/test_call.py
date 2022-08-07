from textwrap import dedent
import unittest

from test_util import test_error

class TestCall(unittest.TestCase):
    def test_bool(self):
        expected = dedent("""\
            [line 1] Can only call functions and classes.
            """)
        test_error(self, 'call/bool.lox', expected, 70)

    def test_nil(self):
        expected = dedent("""\
            [line 1] Can only call functions and classes.
            """)
        test_error(self, 'call/nil.lox', expected, 70)

    def test_num(self):
        expected = dedent("""\
            [line 1] Can only call functions and classes.
            """)
        test_error(self, 'call/num.lox', expected, 70)

    def test_object(self):
        expected = dedent("""\
            [line 4] Can only call functions and classes.
            """)
        test_error(self, 'call/object.lox', expected, 70)

    def test_string(self):
        expected = dedent("""\
            [line 1] Can only call functions and classes.
            """)
        test_error(self, 'call/string.lox', expected, 70)
