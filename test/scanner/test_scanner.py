import unittest

from pylox.scanner.scanner import Scanner
from pylox.scanner.token import TokenType
from pylox.scanner.token import Token

class TestScanner(unittest.TestCase):
    eof_token = Token(TokenType.EOF, '', None, 1)

    def test_scanning_an_arithmetic_expression(self):
        expression = '1 + 2 * 3'
        test_instance = Scanner(expression)
        actual = test_instance.scan_tokens()
        expected = [
            Token(TokenType.NUMBER, '1', 1.0, 1),
            Token(TokenType.PLUS, '+', None, 1),
            Token(TokenType.NUMBER, '2', 2.0, 1),
            Token(TokenType.STAR, '*', None, 1),
            Token(TokenType.NUMBER, '3', 3.0, 1),
            self.eof_token,
        ]

        self.assertEqual(expected, actual)
