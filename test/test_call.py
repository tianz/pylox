from textwrap import dedent
import unittest

from test_util import test_pylox

class TestCall(unittest.TestCase):
    def test_bool(self):
        expected = dedent("""\
            [line 1] Can only call functions and classes.
            """)
        test_pylox(self, 'call/bool.lox', expected)

    def test_nil(self):
        expected = dedent("""\
            [line 1] Can only call functions and classes.
            """)
        test_pylox(self, 'call/nil.lox', expected)

    def test_num(self):
        expected = dedent("""\
            [line 1] Can only call functions and classes.
            """)
        test_pylox(self, 'call/num.lox', expected)

    def test_object(self):
        expected = dedent("""\
            [line 4] Can only call functions and classes.
            """)
        test_pylox(self, 'call/object.lox', expected)

    def test_string(self):
        expected = dedent("""\
            [line 1] Can only call functions and classes.
            """)
        test_pylox(self, 'call/string.lox', expected)