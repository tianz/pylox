from contextlib import redirect_stdout
import io

import lox

def test_pylox(test, input, expected):
    with io.StringIO() as buf, redirect_stdout(buf):
            lox.run_file(f'test/resources/{input}')
            actual = buf.getvalue()

            test.assertEqual(expected, actual)
