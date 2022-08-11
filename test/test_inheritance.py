from textwrap import dedent
import unittest

from test_util import test_pylox, test_error

class TestInheritance(unittest.TestCase):
    def test_constructor(self):
        expected = dedent("""\
            value
            """)
        test_pylox(self, 'inheritance/constructor.lox', expected)

    def test_inherit_from_function(self):
        expected = dedent("""\
            [line 3] Superclass must be a class.
            """)
        test_error(self, 'inheritance/inherit_from_function.lox', expected, 70)

    def test_inherit_from_nil(self):
        expected = dedent("""\
            [line 2] Superclass must be a class.
            """)
        test_error(self, 'inheritance/inherit_from_nil.lox', expected, 70)

    def test_inherit_from_number(self):
        expected = dedent("""\
            [line 2] Superclass must be a class.
            """)
        test_error(self, 'inheritance/inherit_from_number.lox', expected, 70)

    def test_inherit_methods(self):
        expected = dedent("""\
            foo
            bar
            bar
            """)
        test_pylox(self, 'inheritance/inherit_methods.lox', expected)

    def test_parenthesized_superclass(self):
        expected = dedent("""\
            [line 4] Error at '(': Expect superclass name.
            """)
        test_error(self, 'inheritance/parenthesized_superclass.lox', expected, 65)

    def test_set_fields_from_base_class(self):
        expected = dedent("""\
            foo 1
            foo 2
            bar 1
            bar 2
            bar 1
            bar 2
            """)
        test_pylox(self, 'inheritance/set_fields_from_base_class.lox', expected)
