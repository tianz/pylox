from .token import Token, TokenType
import pylox.error.error as ErrorReporter

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
        while not self.__is_at_end():
            self.start = self.current
            self.__scan_token()

        self.tokens.append(Token(TokenType.EOF, '', None, self.line))
        return self.tokens

    def __scan_token(self):
        c = self.__advance()
        match c:
            # single-character tokens
            case '(':
                self.__add_token(TokenType.LEFT_PAREN)
            case ')':
                self.__add_token(TokenType.RIGHT_PAREN)
            case '{':
                self.__add_token(TokenType.LEFT_BRACE)
            case '}':
                self.__add_token(TokenType.RIGHT_BRACE)
            case ',':
                self.__add_token(TokenType.COMMA)
            case '.':
                self.__add_token(TokenType.DOT)
            case '-':
                self.__add_token(TokenType.MINUS)
            case '+':
                self.__add_token(TokenType.PLUS)
            case ';':
                self.__add_token(TokenType.SEMICOLON)
            case '*':
                self.__add_token(TokenType.STAR)
            case '/':
                if self.__match('/'):
                    # a comment gose until the end of the line
                    while self.__peek() != '\n' and not self.__is_at_end():
                        self.__advance()
                else:
                    # only one slash, not a comment
                    self.__add_token(TokenType.SLASH)
            # one or two character tokens
            case '!':
                self.__add_token(TokenType.BANG_EQUAL if self.__match('=') else TokenType.BANG)
            case '=':
                self.__add_token(TokenType.EQUAL_EQUAL if self.__match('=') else TokenType.EQUAL)
            case '<':
                self.__add_token(TokenType.LESS_EQUAL if self.__match('=') else TokenType.LESS)
            case '>':
                self.__add_token(TokenType.GREATER_EQUAL if self.__match('=') else TokenType.GREATER)
                self.__string()
            # whitespaces
            case '\n':
                self.line += 1
            case ' ' | '\r' | '\t':
                pass
            # literals
            case '"':
                self.__string()
            case _:
                if c.isdigit():
                    self.__number()
                elif c.isalpha():
                    self.__identifier()
                else:
                    ErrorReporter.line_error(self.line, 'Unexpected character.')
                    self.had_error = True

    def __string(self):
        while self.__peek() != '"' and not self.__is_at_end():
            if self.__peek() == '\n':
                self.line += 1
            self.__advance()

        if self.__is_at_end():
            ErrorReporter.line_error(self.line, 'Unterminated string.')
            return

        # the closing "
        self.__advance()

        self.__add_token(TokenType.STRING, self.source[self.start + 1 : self.current - 1])

    def __number(self):
        while self.__peek().isdigit():
            self.__advance()

        # look for a fractional part
        if self.__peek() == '.' and self.__peek_next().isdigit():
            # consume the '.'
            self.__advance()

            while self.__peek().isdigit():
                self.__advance()

        self.__add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def __identifier(self):
        while self.__peek().isalnum():
            self.__advance()

        text = self.source[self.start : self.current]
        type = self.keywords.get(text, TokenType.IDENTIFIER)
        self.__add_token(type)

    def __advance(self):
        c = self.source[self.current]
        self.current += 1
        return c

    def __match(self, expected):
        if self.__is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def __peek(self):
        if self.__is_at_end():
            return '\0'
        return self.source[self.current]

    def __peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def __add_token(self, type, literal=None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def __is_at_end(self):
        return self.current >= len(self.source)
