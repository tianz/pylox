from contextlib import redirect_stdout
import io

import lox

def test_pylox(test, input, expected):
    with io.StringIO() as buf, redirect_stdout(buf):
        lox.run_file(f'test/resources/{input}')
        actual = buf.getvalue()

        test.assertEqual(expected, actual)

def test_error(test, input, expected, error_code):
    with io.StringIO() as buf, redirect_stdout(buf):
        with test.assertRaises(SystemExit) as cm:
            lox.run_file(f'test/resources/{input}')

        test.assertEquals(cm.exception.code, error_code)
        test.assertEquals(expected, buf.getvalue())
