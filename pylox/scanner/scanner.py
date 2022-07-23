from .token import Token, TokenType
from ..error.error import report

class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.keywords = {
            'and': TokenType.AND,
            'class': TokenType.CLASS,
            'else': TokenType.ELSE,
            'false': TokenType.FALSE,
            'for': TokenType.FOR,
            'fun': TokenType.FUN,
            'if': TokenType.IF,
            'nil': TokenType.NIL,
            'or': TokenType.OR,
            'print': TokenType.PRINT,
            'return': TokenType.RETURN,
            'super': TokenType.SUPER,
            'this': TokenType.THIS,
            'true': TokenType.TRUE,
            'var': TokenType.VAR,
            'while': TokenType.WHILE,
        }
        self.had_error = False

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, '', None, self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()
        match c:
            # single-character tokens
            case '(':
                self.add_token(TokenType.LEFT_PAREN)
            case ')':
                self.add_token(TokenType.RIGHT_PAREN)
            case '{':
                self.add_token(TokenType.LEFT_BRACE)
            case '}':
                self.add_token(TokenType.RIGHT_BRACE)
            case ',':
                self.add_token(TokenType.COMMA)
            case '.':
                self.add_token(TokenType.DOT)
            case '-':
                self.add_token(TokenType.MINUS)
            case '+':
                self.add_token(TokenType.PLUS)
            case ';':
                self.add_token(TokenType.SEMICOLON)
            case '*':
                self.add_token(TokenType.STAR)
            case '/':
                if self.match('/'):
                    # a comment gose until the end of the line
                    while self.peek() != '\n' and not self.is_at_end():
                        self.advance()
                else:
                    # only one slash, not a comment
                    self.add_token(TokenType.SLASH)
            # one or two character tokens
            case '!':
                self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
            case '=':
                self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
            case '<':
                self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
            case '>':
                self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)
                string()
            # whitespaces
            case '\n':
                self.line += 1
            case ' ' | '\r' | '\t':
                pass
            # literals
            case '"':
                self.string()
            case _:
                if c.isdigit():
                    self.number()
                elif c.isalpha():
                    self.identifier()
                else:
                    error.error(self.line, 'Unexpected character.')
                    self.had_error = True

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_at_end():
            self.__report_error(self.line, 'Unterminated string.')
            return

        # the closing "
        self.advance()

        self.add_token(TokenType.STRING, self.source[self.start + 1 : self.current - 1])

    def number(self):
        while self.peek().isdigit():
            self.advance()

        # look for a fractional part
        if self.peek() == '.' and self.peek_next().is_digit():
            # consume the '.'
            self.advance()

            while self.peek().is_digit():
                self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def identifier(self):
        while self.peek().isalnum():
            self.advance()

        text = self.source[self.start : self.current]
        type = self.keywords.get(text, TokenType.IDENTIFIER)
        self.add_token(type)

    def advance(self):
        c = self.source[self.current]
        self.current += 1
        return c

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def add_token(self, type, literal=None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def is_at_end(self):
        return self.current >= len(self.source)

    def __report_error(self, line, message):
        report(line, "", message)
