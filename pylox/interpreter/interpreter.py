from numpy import isin
from pylox.ast.expr import ExprVisitor
from pylox.scanner.scanner import TokenType
from .runtime_error import RuntimeError

class Interpreter(ExprVisitor):
    def __init__(self):
        self.had_error = False

    def interpret(self, expression):
        try:
            value = self.__evaluate(expression)
            print(self.__stringify(value))
        except RuntimeError as err:
            print(f'{err.message}\n[line {err.token.line}]')
            self.had_error = True

    def visit_binary_expr(self, expr):
        left = self.__evaluate(expr.left)
        right = self.__evaluate(expr.right)

        match expr.operator.type:
            case TokenType.PLUS:
                if isinstance(left, float) and isinstance(right, float):
                    return float(left) + float(right)
                if isinstance(left, str) and isinstance(right, str):
                    return str(left) + str(right)
                raise RuntimeError(expr.operator, 'Operands must be two numbers or two strings.')
            case TokenType.MINUS:
                self.__check_number_operands(expr.operator, left, right)
                return float(left) - float(right)
            case TokenType.STAR:
                self.__check_number_operands(expr.operator, left, right)
                return float(left) * float(right)
            case TokenType.SLASH:
                self.__check_number_operands(expr.operator, left, right)
                return float(left) / float(right)
            case TokenType.GREATER:
                self.__check_number_operands(expr.operator, left, right)
                return float(left) > float(right)
            case TokenType.GREATER_EQUAL:
                self.__check_number_operands(expr.operator, left, right)
                return float(left) >= float(right)
            case TokenType.LESS:
                self.__check_number_operands(expr.operator, left, right)
                return float(left) < float(right)
            case TokenType.LESS_EQUAL:
                self.__check_number_operands(expr.operator, left, right)
                return float(left) <= float(right)
            case TokenType.EQUAL_EQUAL:
                return self.__is_equal(left, right)
            case TokenType.BANG_EQUAL:
                return not self.__is_equal(left, right)

        return None

    def visit_grouping_expr(self, expr):
        return self.__evaluate(expr.expression)

    def visit_literal_expr(self, expr):
        return expr.value

    def visit_unary_expr(self, expr):
        right = self.__evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                self.__check_number_operand(expr.operator, right)
                return -float(right)
            case TokenType.BANG:
                return not self.__is_truthy(right)

        return None

    def __evaluate(self, expr):
        return expr.accept(self)

    def __is_truthy(self, obj):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return bool(obj)

        return True

    def __is_equal(self, a, b):
        if a is None and b is None:
            return True
        if a is None:
            return False

        return a == b

    def __check_number_operand(self, operator, operand):
        if isinstance(operand, float):
            return

        raise RuntimeError(operator, 'Operand must be a number.')

    def __check_number_operands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return

        raise RuntimeError(operator, 'Operands must be a number.')

    def __stringify(self, obj):
        if obj == None:
            return 'nil'
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith('.0'):
                text = text[:len(text) - 2]
            return text

        return str(obj)
