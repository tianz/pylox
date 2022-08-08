from contextlib import redirect_stdout
import io

import lox

def test_pylox(test, input, expected):
    lox.had_error = False
    lox.had_runtime_error = False
    with io.StringIO() as buf, redirect_stdout(buf):
        lox.run_file(f'test/resources/{input}')

        test.assertEqual(expected, buf.getvalue())

def test_error(test, input, expected, error_code):
    lox.had_error = False
    lox.had_runtime_error = False
    with io.StringIO() as buf, redirect_stdout(buf):
        with test.assertRaises(SystemExit) as cm:
            lox.run_file(f'test/resources/{input}')

        test.assertEqual(cm.exception.code, error_code)
        test.assertEqual(expected, buf.getvalue())
