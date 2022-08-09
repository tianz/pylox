from textwrap import dedent
import unittest

from test_util import test_pylox

class TestBool(unittest.TestCase):
    def test_equality(self):
        expected = dedent("""\
            true
            false
            false
            true
            false
            false
            false
            false
            false
            false
            true
            true
            false
            true
            true
            true
            true
            true
            """)
        test_pylox(self, 'bool/equality.lox', expected)

    def test_not(self):
        expected = dedent("""\
            false
            true
            true
            """)
        test_pylox(self, 'bool/not.lox', expected)
