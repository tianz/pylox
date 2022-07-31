from pylox.ast.expr import ExprVisitor
from pylox.ast.stmt import StmtVisitor

class Resolver(ExprVisitor, StmtVisitor):
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes = []

    def visit_block_stmt(self, stmt):
        self.__begin_scope()
        self.__respove(stmt.statements)
        self.__end_scope()
        return None

    def visit_var_stmt(self, stmt):
        self.__declare(stmt.name)
        if stmt.initializer is not None:
            self.__resolve(stmt.initializer)
        self.__define(stmt.name)
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
