from abc import ABC, abstractmethod
from enum import Enum

from .return_value import ReturnValue
from pylox.environment.environment import Environment

class FunctionType(Enum):
    NONE = 1
    FUNCTION = 2
    METHOD = 3
    INITIALIZER = 4

class Callable(ABC):
    @abstractmethod
    def arity(self):
        pass

    @abstractmethod
    def call(self, interperter, arguments):
        pass

class Function(Callable):
    def __init__(self, declaration, closure, is_initializer):
        self.declaration = declaration
        self.closure = closure
        self.is_initializer = is_initializer

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnValue as rv:
            # Found a return statement
            if self.is_initializer:
                return self.closure.get_at(0, 'this')
            return rv.value

        # No return statement
        if self.is_initializer:
            return self.closure.get_at(0, 'this')
        return None

    def bind(self, instance):
        environment = Environment(self.closure)
        environment.define('this', instance)
        return Function(self.declaration, environment, self.is_initializer)

    def __str__(self):
        return f'<fn {self.declaration.name.lexeme}>'
