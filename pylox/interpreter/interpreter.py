from pylox.ast.expr import ExprVisitor
from pylox.ast.stmt import StmtVisitor
from pylox.environment.environment import Environment
from pylox.scanner.scanner import TokenType
from .runtime_error import RuntimeError

class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self):
        self.environment = Environment()
        self.had_error = False

    def interpret(self, statements):
        try:
            for statement in statements:
                self.__execute(statement)
        except RuntimeError as err:
            print(f'{err.message}\n[line {err.token.line}]')
            self.had_error = True

    def visit_assign_expr(self, expr):
        value = self.__evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

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

    def visit_logical_expr(self, expr):
        left = self.__evaluate(expr.left)

        # short circuit: if left is true in an OR expression,
        # or if left is false in an AND expression,
        # just return the left value
        if expr.operator.type == TokenType.OR:
            if self.__is_truthy(left):
                return left
        else:
            if not self.__is_truthy(left):
                return left

        return self.__evaluate(expr.right)

    def visit_unary_expr(self, expr):
        right = self.__evaluate(expr.right)

        match expr.operator.type:
            case TokenType.MINUS:
                self.__check_number_operand(expr.operator, right)
                return -float(right)
            case TokenType.BANG:
                return not self.__is_truthy(right)

        return None

    def visit_variable_expr(self, expr):
        return self.environment.get(expr.name)

    def visit_block_stmt(self, stmt):
        self.__execute_block(stmt.statements, Environment(self.environment))

    def visit_expression_stmt(self, stmt):
        self.__evaluate(stmt.expression)
        return None

    def visit_if_stmt(self, stmt):
        if self.__is_truthy(self.__evaluate(stmt.condition)):
            self.__execute(stmt.then_branch)
        elif stmt.else_branch:
            self.__execute(stmt.else_branch)

        return None

    def visit_print_stmt(self, stmt):
        value = self.__evaluate(stmt.expression)
        print(self.__stringify(value))
        return None

    def visit_var_stmt(self, stmt):
        value = None
        if stmt.initializer != None:
            value = self.__evaluate(stmt.initializer)

        self.environment.define(stmt.name.lexeme, value)
        return None

    def visit_while_stmt(self, stmt):
        while self.__is_truthy(self.__evaluate(stmt.condition)):
            self.__execute(stmt.body)

        return None

    def __evaluate(self, expr):
        return expr.accept(self)

    def __execute_block(self, statements, environment):
        previous_env = self.environment

        try:
            self.environment = environment
            for statement in statements:
                self.__execute(statement)
        finally:
            self.environment = previous_env

    def __execute(self, stmt):
        return stmt.accept(self)

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
        if isinstance(obj, bool):
            return str(obj).lower()

        return str(obj)
