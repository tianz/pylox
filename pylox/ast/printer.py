from .expr import ExprVisitor

class AstPrinter(ExprVisitor):
    def print(self, expr):
        return expr.accept(self)

    def visit_binary_expr(self, expr):
        return self.__parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr):
        return self.__parenthesize('grouping', expr.expression)

    def visit_literal_expr(self, expr):
        if expr.value is None:
            return 'nil'

        return str(expr.value)

    def visit_unary_expr(self, expr):
        return self.__parenthesize(expr.operator.lexeme, expr.right)

    def __parenthesize(self, name, *exprs):
        str_builder = ['(', name]

        for expr in exprs:
            str_builder.append(' ')
            str_builder.append(expr.accept(self))

        str_builder.append(')')

        return ''.join(str_builder)
