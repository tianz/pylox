import unittest

from pylox.scanner.scanner import Scanner
from pylox.scanner.token import TokenType
from pylox.scanner.token import Token

class TestScanner(unittest.TestCase):
    eof_token = Token(TokenType.EOF, '', None, 1)

    def test_plus_and_minus(self):
        expression = '1 + 2 - 3'
        test_instance = Scanner(expression)
        actual = test_instance.scan_tokens()
        expected = [
            Token(TokenType.NUMBER, '1', 1.0, 1),
            Token(TokenType.PLUS, '+', None, 1),
            Token(TokenType.NUMBER, '2', 2.0, 1),
            Token(TokenType.MINUS, '-', None, 1),
            Token(TokenType.NUMBER, '3', 3.0, 1),
            self.eof_token,
        ]

        self.assertEqual(expected, actual)

    def test_multiply_and_divide(self):
        expression = '1 * 2.3 / 4.0'
        test_instance = Scanner(expression)
        actual = test_instance.scan_tokens()
        expected = [
            Token(TokenType.NUMBER, '1', 1.0, 1),
            Token(TokenType.STAR, '*', None, 1),
            Token(TokenType.NUMBER, '2.3', 2.3, 1),
            Token(TokenType.SLASH, '/', None, 1),
            Token(TokenType.NUMBER, '4.0', 4.0, 1),
            self.eof_token,
        ]

        self.assertEqual(expected, actual)

    def test_parentheses(self):
        expression = '(1 + 20)'
        test_instance = Scanner(expression)
        actual = test_instance.scan_tokens()
        expected = [
            Token(TokenType.LEFT_PAREN, '(', None, 1),
            Token(TokenType.NUMBER, '1', 1.0, 1),
            Token(TokenType.PLUS, '+', None, 1),
            Token(TokenType.NUMBER, '20', 20.0, 1),
            Token(TokenType.RIGHT_PAREN, ')', None, 1),
            self.eof_token,
        ]

        self.assertEqual(expected, actual)

    def test_block(self):
        block = '{\n a = "a";\n }'
        test_instance = Scanner(block)
        actual = test_instance.scan_tokens()
        expected = [
            Token(TokenType.LEFT_BRACE, '{', None, 1),
            Token(TokenType.IDENTIFIER, 'a', None, 2),
            Token(TokenType.EQUAL, '=', None, 2),
            Token(TokenType.STRING, '"a"', 'a', 2),
            Token(TokenType.SEMICOLON, ';', None, 2),
            Token(TokenType.RIGHT_BRACE, '}', None, 3),
            Token(TokenType.EOF, '', None, 3),
        ]

        self.assertEqual(expected, actual)


    def test_equality(self):
        expression = 'value == a'
        test_instance = Scanner(expression)
        actual = test_instance.scan_tokens()
        expected = [
            Token(TokenType.IDENTIFIER, 'value', None, 1),
            Token(TokenType.EQUAL_EQUAL, '==', None, 1),
            Token(TokenType.IDENTIFIER, 'a', None, 1),
            self.eof_token,
        ]

        self.assertEqual(expected, actual)

    def test_inequality(self):
        expression = 'a != b'
        test_instance = Scanner(expression)
        actual = test_instance.scan_tokens()
        expected = [
            Token(TokenType.IDENTIFIER, 'a', None, 1),
            Token(TokenType.BANG_EQUAL, '!=', None, 1),
            Token(TokenType.IDENTIFIER, 'b', None, 1),
            self.eof_token,
        ]

        self.assertEqual(expected, actual)

    def test_comment(self):
        expression = '// this is a comment'
        test_instance = Scanner(expression)
        actual = test_instance.scan_tokens()
        expected = [
            self.eof_token,
        ]

        self.assertEqual(expected, actual)

    def test_whitespaces(self):
        expression = '  \r\t\n'
        test_instance = Scanner(expression)
        actual = test_instance.scan_tokens()
        expected = [
            Token(TokenType.EOF, '', None, 2),
        ]

        self.assertEqual(expected, actual)
