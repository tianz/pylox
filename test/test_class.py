from textwrap import dedent
import unittest

from test_util import test_pylox, test_error

class TestClass(unittest.TestCase):
    def test_empty(self):
        expected = dedent("""\
            Foo
            """)
        test_pylox(self, 'class/empty.lox', expected)

    def test_inherit_self(self):
        expected = dedent("""\
            [line 1] Error at 'Foo': A class can't inherit from itself.
            """)
        test_error(self, 'class/inherit_self.lox', expected, 65)

    def test_inherited_method(self):
        expected = dedent("""\
            in foo
            in bar
            in baz
            """)
        test_pylox(self, 'class/inherited_method.lox', expected)

    def test_local_inherit_other(self):
        expected = dedent("""\
            B
            """)
        test_pylox(self, 'class/local_inherit_other.lox', expected)

    def test_local_inherit_self(self):
        expected = dedent("""\
            [line 2] Error at 'Foo': A class can't inherit from itself.
            """)
        test_error(self, 'class/local_inherit_self.lox', expected, 65)

    def test_local_reference_self(self):
        expected = dedent("""\
            Foo
            """)
        test_pylox(self, 'class/local_reference_self.lox', expected)

    def test_reference_self(self):
        expected = dedent("""\
            Foo
            """)
        test_pylox(self, 'class/reference_self.lox', expected)
