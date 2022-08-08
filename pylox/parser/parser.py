from pylox.scanner.token import TokenType
import pylox.ast.expr as Expr
import pylox.ast.stmt as Stmt
from .parser_error import ParserError
import pylox.error.error as ErrorReporter

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
            if self.__match(TokenType.CLASS):
                return self.__class_declaration()
            if self.__match(TokenType.FUN):
                return self.__function('function')
            if self.__match(TokenType.VAR):
                return self.__var_declaration()
            return self.__statement()
        except ParserError:
            self.__synchronize()
            return None

    def __class_declaration(self):
        name = self.__consume(TokenType.IDENTIFIER, 'Expect class name.')

        superclass = None
        if self.__match(TokenType.LESS):
            self.__consume(TokenType.IDENTIFIER, 'Expect superclass name.')
            superclass = Expr.Variable(self.__previous())

        self.__consume(TokenType.LEFT_BRACE, "Expect '(' before class body.")
        methods = []

        while not self.__check(TokenType.RIGHT_BRACE) and not self.__is_at_end():
            methods.append(self.__function('method'))

        self.__consume(TokenType.RIGHT_BRACE, "Expect '}' after class body.")

        return Stmt.Class(name, superclass, methods)

    def __function(self, kind):
        # header
        name = self.__consume(TokenType.IDENTIFIER, f'Expect {kind} name.')
        self.__consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")
        parameters = []

        if not self.__check(TokenType.RIGHT_PAREN):
            parameters.append(self.__consume(TokenType.IDENTIFIER, 'Expect parameter name.'))

            while self.__match(TokenType.COMMA):
                if (len(parameters) >= 255):
                    self.__error(self.__peek(), "Can't have more than 255 parameters.")
                parameters.append(self.__consume(TokenType.IDENTIFIER, 'Expect parameter name.'))

        self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")

        # body
        self.__consume(TokenType.LEFT_BRACE, f"Expect '{{' before {kind} body.")
        body = self.__block()

        return Stmt.Function(name, parameters, body)

    def __var_declaration(self):
        name = self.__consume(TokenType.IDENTIFIER, 'Expect variable name.')
        initializer = self.__expression() if self.__match(TokenType.EQUAL) else None
        self.__consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Stmt.Var(name, initializer)

    def __statement(self):
        if self.__match(TokenType.FOR):
            return self.__for_statement()
        if self.__match(TokenType.IF):
            return self.__if_statement()
        if self.__match(TokenType.PRINT):
            return self.__print_statement()
        if self.__match(TokenType.RETURN):
            return self.__return_statement()
        if self.__match(TokenType.WHILE):
            return self.__while_statement()
        if self.__match(TokenType.LEFT_BRACE):
            return Stmt.Block(self.__block())

        return self.__expression_statement()

    def __expression_statement(self):
        expr = self.__expression()
        self.__consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Stmt.Expression(expr)

    def __for_statement(self):
        self.__consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")

        if self.__match(TokenType.SEMICOLON):
            initializer = None
        elif self.__match(TokenType.VAR):
            # loop counter is declared here
            initializer = self.__var_declaration()
        else:
            # loop counter is declared above
            initializer = self.__expression_statement()

        condition = None
        if not self.__check(TokenType.SEMICOLON):
            condition = self.__expression()
        self.__consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment = None
        if not self.__check(TokenType.RIGHT_PAREN):
            increment = self.__expression()
        self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        body = self.__statement()
        if increment:
            body = Stmt.Block([body, Stmt.Expression(increment)])
        if condition:
            body = Stmt.While(condition, body)
        if initializer:
            body = Stmt.Block([initializer, body])

        return body

    def __if_statement(self):
        self.__consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.__expression()
        self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self.__statement()
        else_branch = None
        if self.__match(TokenType.ELSE):
            else_branch = self.__statement()

        return Stmt.If(condition, then_branch, else_branch)

    def __print_statement(self):
        value = self.__expression()
        self.__consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Stmt.Print(value)

    def __return_statement(self):
        keyword = self.__previous()
        value = None
        if not self.__check(TokenType.SEMICOLON):
            value = self.__expression()

        self.__consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return Stmt.Return(keyword, value)

    def __while_statement(self):
        self.__consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.__expression()
        self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after 'while'.")
        body = self.__statement()

        return Stmt.While(condition, body)

    def __block(self):
        statements = []

        while not self.__check(TokenType.RIGHT_BRACE) and not self.__is_at_end():
            statements.append(self.__declaration())

        self.__consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def __expression(self):
        return self.__assignment()

    def __assignment(self):
        expr = self.__or()

        if self.__match(TokenType.EQUAL):
            equals = self.__previous()
            value = self.__assignment()

            if isinstance(expr, Expr.Variable):
                return Expr.Assign(expr.name, value)
            elif isinstance(expr, Expr.Get):
                return Expr.Set(expr.object, expr.name, value)

            ErrorReporter.token_error(equals, 'Invalid assignment target.')
            self.had_error = True

        return expr

    def __or(self):
        expr = self.__and()

        if self.__match(TokenType.OR):
            operator = self.__previous()
            right = self.__and()
            expr = Expr.Logical(expr, operator, right)

        return expr

    def __and(self):
        expr = self.__equality()

        if self.__match(TokenType.AND):
            operator = self.__previous()
            right = self.__equality()
            expr = Expr.Logical(expr, operator, right)

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

        return self.__call()

    def __call(self):
        def finish_call(callee):
            arguments = []

            if not self.__check(TokenType.RIGHT_PAREN):
                arguments = [self.__expression()]
                while self.__match(TokenType.COMMA):
                    arguments.append(self.__expression())

                    if len(arguments) >= 255:
                        self.__error(self.__peek(), "Can't have more than 255 arguments.")

            right_paren = self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
            return Expr.Call(callee, right_paren, arguments)

        expr = self.__primary()

        while True:
            if self.__match(TokenType.LEFT_PAREN):
                expr = finish_call(expr)
            elif self.__match(TokenType.DOT):
                name = self.__consume(TokenType.IDENTIFIER, "Expect property name after '.'.")
                expr = Expr.Get(expr, name)
            else:
                break

        return expr

    def __primary(self):
        if self.__match(TokenType.FALSE):
            return Expr.Literal(False)
        if self.__match(TokenType.TRUE):
            return Expr.Literal(True)
        if self.__match(TokenType.NIL):
            return Expr.Literal(None)
        if self.__match(TokenType.NUMBER, TokenType.STRING):
            return Expr.Literal(self.__previous().literal)
        if self.__match(TokenType.SUPER):
            keyword = self.__previous()
            self.__consume(TokenType.DOT, "Expect '.' after 'super'.")
            method = self.__consume(TokenType.IDENTIFIER, 'Expect superclass method name.')
            return Expr.Super(keyword, method)
        if self.__match(TokenType.THIS):
            return Expr.This(self.__previous())
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
        ErrorReporter.token_error(token, message)
        self.had_error = True
        return ParserError()

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
