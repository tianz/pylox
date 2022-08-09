from textwrap import dedent
import unittest

from test_util import test_pylox, test_error

class TestField(unittest.TestCase):
    def test_call_function_field(self):
        expected = dedent("""\
            bar
            1
            2
            """)
        test_pylox(self, 'field/call_function_field.lox', expected)

    def test_call_nonfunction_field(self):
        expected = dedent("""\
            [line 6] Can only call functions and classes.
            """)
        test_error(self, 'field/call_nonfunction_field.lox', expected, 70)

    def test_get_and_set_method(self):
        expected = dedent("""\
            other
            1
            method
            2
            """)
        test_pylox(self, 'field/get_and_set_method.lox', expected)

    def test_get_on_bool(self):
        expected = dedent("""\
            [line 1] Only instances have properties.
            """)
        test_error(self, 'field/get_on_bool.lox', expected, 70)

    def test_get_on_class(self):
        expected = dedent("""\
            [line 2] Only instances have properties.
            """)
        test_error(self, 'field/get_on_class.lox', expected, 70)

    def test_get_on_function(self):
        expected = dedent("""\
            [line 3] Only instances have properties.
            """)
        test_error(self, 'field/get_on_function.lox', expected, 70)

    def test_get_on_nil(self):
        expected = dedent("""\
            [line 1] Only instances have properties.
            """)
        test_error(self, 'field/get_on_nil.lox', expected, 70)

    def test_get_on_num(self):
        expected = dedent("""\
            [line 1] Only instances have properties.
            """)
        test_error(self, 'field/get_on_num.lox', expected, 70)

    def test_get_on_string(self):
        expected = dedent("""\
            [line 1] Only instances have properties.
            """)
        test_error(self, 'field/get_on_string.lox', expected, 70)

    def test_many(self):
        expected = dedent("""\
            apple
            apricot
            avocado
            banana
            bilberry
            blackberry
            blackcurrant
            blueberry
            boysenberry
            cantaloupe
            cherimoya
            cherry
            clementine
            cloudberry
            coconut
            cranberry
            currant
            damson
            date
            dragonfruit
            durian
            elderberry
            feijoa
            fig
            gooseberry
            grape
            grapefruit
            guava
            honeydew
            huckleberry
            jabuticaba
            jackfruit
            jambul
            jujube
            juniper
            kiwifruit
            kumquat
            lemon
            lime
            longan
            loquat
            lychee
            mandarine
            mango
            marionberry
            melon
            miracle
            mulberry
            nance
            nectarine
            olive
            orange
            papaya
            passionfruit
            peach
            pear
            persimmon
            physalis
            pineapple
            plantain
            plum
            plumcot
            pomegranate
            pomelo
            quince
            raisin
            rambutan
            raspberry
            redcurrant
            salak
            salmonberry
            satsuma
            strawberry
            tamarillo
            tamarind
            tangerine
            tomato
            watermelon
            yuzu
            """)
        test_pylox(self, 'field/many.lox', expected)

    def test_method(self):
        expected = dedent("""\
            got method
            arg
            """)
        test_pylox(self, 'field/method.lox', expected)

    def test_method_binds_this(self):
        expected = dedent("""\
            foo1
            1
            """)
        test_pylox(self, 'field/method_binds_this.lox', expected)

    def test_on_instance(self):
        expected = dedent("""\
            bar value
            baz value
            bar value
            baz value
            """)
        test_pylox(self, 'field/on_instance.lox', expected)

    def test_set_evaluation_order(self):
        expected = dedent("""\
            [line 1] Undefined variable 'undefined1'.
            """)
        test_error(self, 'field/set_evaluation_order.lox', expected, 70)

    def test_set_on_bool(self):
        expected = dedent("""\
            [line 1] Only instances have fields.
            """)
        test_error(self, 'field/set_on_bool.lox', expected, 70)

    def test_set_on_class(self):
        expected = dedent("""\
            [line 2] Only instances have fields.
            """)
        test_error(self, 'field/set_on_class.lox', expected, 70)

    def test_set_on_function(self):
        expected = dedent("""\
            [line 3] Only instances have fields.
            """)
        test_error(self, 'field/set_on_function.lox', expected, 70)

    def test_set_on_nil(self):
        expected = dedent("""\
            [line 1] Only instances have fields.
            """)
        test_error(self, 'field/set_on_nil.lox', expected, 70)

    def test_set_on_num(self):
        expected = dedent("""\
            [line 1] Only instances have fields.
            """)
        test_error(self, 'field/set_on_num.lox', expected, 70)

    def test_set_on_string(self):
        expected = dedent("""\
            [line 1] Only instances have fields.
            """)
        test_error(self, 'field/set_on_string.lox', expected, 70)

    def test_undefined(self):
        expected = dedent("""\
            [line 4] Undefined property 'bar'.
            """)
        test_error(self, 'field/undefined.lox', expected, 70)
