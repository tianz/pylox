from re import L
from pylox.scanner.token import TokenType
import pylox.ast.expr as Expr
import pylox.ast.stmt as Stmt
from .parser_error import ParserError
from ..error.error import report

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.had_error = False

    def parse(self):
        statements = []
        while not self.__is_at_end():
            statements.append(self.__declaration())

        return statements

    def __declaration(self):
        try:
            if self.__match(TokenType.VAR):
                return self.__var_declaration()
            return self.__statement()
        except ParserError:
            self.__synchronize()
            return None

    def __var_declaration(self):
        name = self.__consume(TokenType.IDENTIFIER, 'Expect variable name.')
        initializer = self.__expression() if self.__match(TokenType.EQUAL) else None
        self.__consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Stmt.Var(name, initializer)

    def __statement(self):
        if self.__match(TokenType.PRINT):
            return self.__print_statement()
        if self.__match(TokenType.LEFT_BRACE):
            return Stmt.Block(self.__block())

        return self.__expression_statement()

    def __expression_statement(self):
        expr = self.__expression()
        self.__consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Stmt.Expression(expr)

    def __if_statement(self):
        self.__consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.__expression()
        self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self.__statement()
        else_branch = None
        if (self.__match(TokenType.ELSE)):
            else_branch = self.__statement()

        return Stmt.If(condition, then_branch, else_branch)

    def __print_statement(self):
        value = self.__expression()
        self.__consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Stmt.Print(value)

    def __block(self):
        statements = []

        while not self.__check(TokenType.RIGHT_BRACE) and not self.__is_at_end():
            statements.append(self.__declaration())

        self.__consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def __expression(self):
        return self.__assignment()

    def __assignment(self):
        expr = self.__equality()

        if self.__match(TokenType.EQUAL):
            equals = self.__previous()
            value = self.__assignment()

            if isinstance(expr, Expr.Variable):
                name = expr.name
                return Expr.Assign(name, value)

            self.__report_error(equals, 'Invalid assignment target.')

        return expr

    def __equality(self):
        expr = self.__comparison()

        while self.__match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.__previous()
            right = self.__comparison()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def __comparison(self):
        expr = self.__term()

        while self.__match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.__previous()
            right = self.__term()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def __term(self):
        expr = self.__factor()

        while self.__match(TokenType.MINUS, TokenType.PLUS):
            operator = self.__previous()
            right = self.__factor()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def __factor(self):
        expr = self.__unary()

        while self.__match(TokenType.SLASH, TokenType.STAR):
            operator = self.__previous()
            right = self.__unary()
            expr = Expr.Binary(expr, operator, right)

        return expr

    def __unary(self):
        if self.__match(TokenType.BANG, TokenType.MINUS):
            operator = self.__previous()
            right = self.__unary()
            return Expr.Unary(operator, right)

        return self.__primary()

    def __primary(self):
        if self.__match(TokenType.FALSE):
            return Expr.Literal(False)
        if self.__match(TokenType.TRUE):
            return Expr.Literal(True)
        if self.__match(TokenType.NIL):
            return Expr.Literal(None)
        if self.__match(TokenType.NUMBER, TokenType.STRING):
            return Expr.Literal(self.__previous().literal)
        if self.__match(TokenType.IDENTIFIER):
            return Expr.Variable(self.__previous())
        if self.__match(TokenType.LEFT_PAREN):
            expr = self.__expression()
            self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)

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
        return self.__peek().type == TokenType.EOF
