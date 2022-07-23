from pylox.scanner.token import TokenType
from pylox.ast.expr import Binary, Grouping, Literal, Unary
from .parser_error import ParserError
from ..error.error import report

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.had_error = False

    def parse(self):
        try:
            return self.__expression()
        except ParserError:
            return None

    def __expression(self):
        return self.__equality()

    def __equality(self):
        expr = self.__comparison()

        while self.__match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.__previous()
            right = self.__comparison()
            expr = Binary(expr, operator, right)

        return expr

    def __comparison(self):
        expr = self.__term()

        while self.__match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.__previous()
            right = self.__term()
            expr = Binary(expr, operator, right)

        return expr

    def __term(self):
        expr = self.__factor()

        while self.__match(TokenType.MINUS, TokenType.PLUS):
            operator = self.__previous()
            right = self.__factor()
            expr = Binary(expr, operator, right)

        return expr

    def __factor(self):
        expr = self.__unary()

        while self.__match(TokenType.SLASH, TokenType.STAR):
            operator = self.__previous()
            right = self.__unary()
            expr = Binary(expr, operator, right)

        return expr

    def __unary(self):
        if self.__match(TokenType.BANG, TokenType.MINUS):
            operator = self.__previous()
            right = self.__unary()
            return Unary(operator, right)

        return self.__primary()

    def __primary(self):
        if self.__match(TokenType.FALSE):
            return Literal(False)
        if self.__match(TokenType.TRUE):
            return Literal(True)
        if self.__match(TokenType.NIL):
            return Literal(None)
        if self.__match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.__previous().literal)
        if self.__match(TokenType.LEFT_PAREN):
            expr = self.__expression()
            self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

        raise self.__error(self.__peek(), 'Expect expression.')

    def __match(self, *types):
        for type in types:
            if self.__check(type):
                self.__advance()
                return True

        return False

    def __consume(self, type, message):
        if self.__check(type):
            return self.__advance()

        raise self.__error(self.__peek(), message)

    def __check(self, type):
        if self.__is_at_end():
            return False

        return self.__peek().type == type

    def __advance(self):
        if not self.__is_at_end():
            self.current += 1

        return self.__previous()

    def __peek(self):
        return self.tokens[self.current]

    def __previous(self):
        return self.tokens[self.current - 1]

    def __error(self, token, message):
        self.had_error = True
        self.__report_error(token, message)
        return ParserError()

    def __report_error(self, token, message):
        if token.type == TokenType.EOF:
            report(token.line, ' at end', message)
        else:
            report(token.line, " at '" + token.lexeme + "'", message)

    def __synchronize(self):
        self.__advance()

        while not self.__is_at_end():
            if self.__previous().type == TokenType.SEMICOLON:
                return

            match self.__peek().type:
                case TokenType.CLASS, TokenType.FUN, TokenType.VAR, TokenType.FOR, TokenType.IF, TokenType.WHILE, \
                        TokenType.PRINT, TokenType.RETURN:
                    return

            self.__advance()

    def __is_at_end(self):
        return self.__peek() == TokenType.EOF
