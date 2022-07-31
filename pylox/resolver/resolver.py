from pylox.ast.expr import ExprVisitor
from pylox.ast.stmt import StmtVisitor
import pylox.error.error as ErrorReporter

class Resolver(ExprVisitor, StmtVisitor):
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes = []

    def visit_block_stmt(self, stmt):
        self.__begin_scope()
        self.__resolve(stmt.statements)
        self.__end_scope()
        return None

    def visit_expression_stmt(self, stmt):
        self.__resolve(stmt.expression)
        return None

    def visit_function_stmt(self, stmt):
        self.__declare(stmt.name)
        self.__define(stmt.name) # define the function to allow recursion
        self.__resolve_function(stmt)
        return None

    def visit_if_stmt(self, stmt):
        self.__resolve(stmt.condition)
        self.__resolve(stmt.then_branch)
        if stmt.else_branch:
            self.__resolve(stmt.else_branch)
        return None

    def visit_print_stmt(self, stmt):
        self.__resolve(stmt.expression)
        return None

    def visit_return_stmt(self, stmt):
        if stmt.value is not None:
            self.__resolve(stmt.value)
        return None

    def visit_var_stmt(self, stmt):
        self.__declare(stmt.name)
        if stmt.initializer is not None:
            self.__resolve(stmt.initializer)
        self.__define(stmt.name)
        return None

    def visit_while_stmt(self, stmt):
        self.__resolve(stmt.condition)
        self.__resolve(stmt.body)
        return None

    def visit_assignment_expr(self, expr):
        self.__resolve(expr.value)
        self.__resolve_local(expr, expr.name)
        return None

    def visit_binary_expr(self, expr):
        self.__resolve(expr.left)
        self.__resolve(expr.right)
        return None

    def visit_call_expr(self, expr):
        self.__resolve(expr.callee)
        for argument in expr.araguments:
            self.__resolve(argument)
        return None

    def visit_grouping_expr(self, expr):
        self.__resolve(expr.expression)
        return None

    def visit_literal_expr(self, expr):
        return None

    def visit_logical_expr(self, expr):
        self.__resolve(expr.left)
        self.__resolve(expr.right)
        return None

    def visit_unary_expr(self, expr):
        self.__resolve(expr.right)
        return None

    def visit_variable_expr(self, expr):
        if self.scopes and not self.scopes[-1][expr.name.lexeme]:
            ErrorReporter.token_error(expr.name, "Can't read local variable in its own initializer.")

        self.__resolve_local(expr, expr.name)
        return None

    def __begin_scope(self):
        self.scopes.append({})

    def __end_scope(self):
        self.scopes.pop()

    def __resolve(self, statements):
        for statement in statements:
            self.__resolve(statement)

    def __resolve(self, stmt_or_expr):
        stmt_or_expr.accept(self)

    def __declare(self, name_token):
        if not self.scopes:
            return

        self.scopes[-1][name_token.lexeme] = False # False means the name is not initialized

    def __define(self, name_token):
        if not self.scopes:
            return

        self.scopes[-1][name_token.lexeme] = True

    def __resolve_local(self, expr, name):
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return

    def __resolve_function(self, function):
        self.__begin_scope()
        for param in function.params:
            self.__declare(param)
            self.__define(param)

        self.__resolve(function.body)
        self.__end_scope()