from textwrap import dedent
import unittest

from test_util import test_pylox

class TestClosure(unittest.TestCase):
    def test_assign_to_closure(self):
        expected = dedent("""\
            local
            after f
            after f
            after g
            """)
        test_pylox(self, 'closure/assign_to_closure.lox', expected)

    def test_assign_to_shadowed_later(self):
        expected = dedent("""\
            inner
            assigned
            """)
        test_pylox(self, 'closure/assign_to_shadowed_later.lox', expected)

    def test_close_over_function_parameter(self):
        expected = dedent("""\
            param
            """)
        test_pylox(self, 'closure/close_over_function_parameter.lox', expected)

    def test_close_over_later_variable(self):
        expected = dedent("""\
            b
            a
            """)
        test_pylox(self, 'closure/close_over_later_variable.lox', expected)

    def test_close_over_method_parameter(self):
        expected = dedent("""\
            param
            """)
        test_pylox(self, 'closure/close_over_method_parameter.lox', expected)

    def test_closed_closure_in_function(self):
        expected = dedent("""\
            local
            """)
        test_pylox(self, 'closure/closed_closure_in_function.lox', expected)

    def test_nested_closure(self):
        expected = dedent("""\
            a
            b
            c
            """)
        test_pylox(self, 'closure/nested_closure.lox', expected)

    def test_open_closure_in_function(self):
        expected = dedent("""\
            local
            """)
        test_pylox(self, 'closure/open_closure_in_function.lox', expected)

    def test_reference_closure_multiple_times(self):
        expected = dedent("""\
            a
            a
            """)
        test_pylox(self, 'closure/reference_closure_multiple_times.lox', expected)

    def test_reuse_closure_slot(self):
        expected = dedent("""\
            a
            """)
        test_pylox(self, 'closure/reuse_closure_slot.lox', expected)

    def test_shadow_closure_with_local(self):
        expected = dedent("""\
            closure
            shadow
            closure
            """)
        test_pylox(self, 'closure/shadow_closure_with_local.lox', expected)

    def test_unused_closure(self):
        expected = dedent("""\
            ok
            """)
        test_pylox(self, 'closure/unused_closure.lox', expected)

    def test_unused_later_closure(self):
        expected = dedent("""\
            a
            """)
        test_pylox(self, 'closure/unused_later_closure.lox', expected)
