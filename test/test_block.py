from textwrap import dedent
import unittest

from test_util import test_pylox

class TestBlock(unittest.TestCase):
    def test_empty(self):
        expected = dedent("""\
            ok
            """)
        test_pylox(self, 'block/empty.lox', expected)

    def test_scope(self):
        expected = dedent("""\
            inner
            outer
            """)
        test_pylox(self, 'block/scope.lox', expected)
