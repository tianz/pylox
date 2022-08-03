from pylox.ast.expr import ExprVisitor
from pylox.ast.stmt import StmtVisitor
import pylox.error.error as ErrorReporter
from pylox.function.function import FunctionType
from pylox.lox_class.lox_class import ClassType

class Resolver(ExprVisitor, StmtVisitor):
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes = []
        self.current_function = FunctionType.NONE
        self.current_class = ClassType.NONE
        self.had_error = False

    def visit_block_stmt(self, stmt):
        self.__begin_scope()
        self.resolve(stmt.statements)
        self.__end_scope()
        return None

    def visit_class_stmt(self, stmt):
        enclosing_class = self.current_class
        self.current_class = ClassType.CLASS
        self.__declare(stmt.name)
        self.__define(stmt.name)

        if stmt.superclass is not None:
            if stmt.name.lexeme == stmt.superclass.name.lexeme:
                ErrorReporter.token_error(stmt.superclass.name, "A class can't inherit from itself.")
                self.had_error = True

            self.current_class = ClassType.SUBCLASS
            self.__resolve(stmt.superclass)

            self.__begin_scope()
            self.scopes[-1]['super'] = True

        self.__begin_scope()
        self.scopes[-1]['this'] = True

        for method in stmt.methods:
            function_type = FunctionType.METHOD
            if method.name.lexeme == 'init':
                function_type = FunctionType.INITIALIZER

            self.__resolve_function(method, function_type)

        self.__end_scope()

        if stmt.superclass is not None:
            self.__end_scope()

        self.current_class = enclosing_class
        return None

    def visit_expression_stmt(self, stmt):
        self.__resolve(stmt.expression)
        return None

    def visit_function_stmt(self, stmt):
        self.__declare(stmt.name)
        self.__define(stmt.name) # define the function to allow recursion
        self.__resolve_function(stmt, FunctionType.FUNCTION)
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
        if self.current_function == FunctionType.NONE:
            ErrorReporter.token_error(stmt.keyword, "Can't return from top-level code.")
            self.had_error = True

        if stmt.value is not None:
            if self.current_function == FunctionType.INITIALIZER:
                ErrorReporter.token_error(stmt.keyword, "Can't return a value from an initializer.")
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

    def visit_assign_expr(self, expr):
        self.__resolve(expr.value)
        self.__resolve_local(expr, expr.name)
        return None

    def visit_binary_expr(self, expr):
        self.__resolve(expr.left)
        self.__resolve(expr.right)
        return None

    def visit_call_expr(self, expr):
        self.__resolve(expr.callee)
        for argument in expr.arguments:
            self.__resolve(argument)
        return None

    def visit_get_expr(self, expr):
        self.__resolve(expr.object)
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

    def visit_set_expr(self, expr):
        self.__resolve(expr.value)
        self.__resolve(expr.object)
        return None

    def visit_super_expr(self, expr):
        if self.current_class == ClassType.NONE:
            ErrorReporter.token_error(expr.keyword, "Can't use 'super' outside of a class.")
            self.had_error = True
        elif self.current_class != ClassType.SUBCLASS:
            ErrorReporter.token_error(expr.keyword, "Can't use 'super' in a class with no superclass.")
            self.had_error = True

        self.__resolve_local(expr, expr.keyword)
        return None

    def visit_this_expr(self, expr):
        if self.current_class == ClassType.NONE:
            ErrorReporter.token_error(expr.keyword, "Can't use 'this' outside of a class.")
            self.had_error = True
            return None

        self.__resolve_local(expr, expr.keyword)
        return None

    def visit_unary_expr(self, expr):
        self.__resolve(expr.right)
        return None

    def visit_variable_expr(self, expr):
        if self.scopes and not self.scopes[-1][expr.name.lexeme]:
            ErrorReporter.token_error(expr.name, "Can't read local variable in its own initializer.")
            self.had_error = True

        self.__resolve_local(expr, expr.name)
        return None

    def resolve(self, statements):
        for statement in statements:
            self.__resolve(statement)

    def __begin_scope(self):
        self.scopes.append({})

    def __end_scope(self):
        self.scopes.pop()

    def __resolve(self, stmt_or_expr):
        stmt_or_expr.accept(self)

    def __declare(self, name_token):
        if not self.scopes:
            return

        if name_token.lexeme in self.scopes[-1]:
            ErrorReporter.token_error(name_token, 'Already a variable with this name in this scope.')
            self.had_error = True

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

    def __resolve_function(self, function, function_type):
        enclosing_function = self.current_function
        self.current_function = function_type

        self.__begin_scope()
        for param in function.params:
            self.__declare(param)
            self.__define(param)

        self.resolve(function.body)
        self.__end_scope()
        self.current_function = enclosing_function
