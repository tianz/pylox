from textwrap import dedent
import unittest

from test_util import test_pylox

class TestComments(unittest.TestCase):
    def test_line_at_eof(self):
        expected = dedent("""\
            ok
            """)
        test_pylox(self, 'comments/line_at_eof.lox', expected)

    def test_only_line_comment(self):
        expected = ''
        test_pylox(self, 'comments/only_line_comment.lox', expected)

    def test_only_line_comment_and_line(self):
        expected = ''
        test_pylox(self, 'comments/only_line_comment_and_line.lox', expected)

    def test_unicode(self):
        expected = dedent("""\
            ok
            """)
        test_pylox(self, 'comments/unicode.lox', expected)
