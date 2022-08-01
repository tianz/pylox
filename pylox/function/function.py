from abc import ABC, abstractmethod
from enum import Enum

from .return_value import ReturnValue
from pylox.environment.environment import Environment

class FunctionType(Enum):
    NONE = 1
    FUNCTION = 2
    METHOD = 3

class Callable(ABC):
    @abstractmethod
    def arity(self):
        pass

    @abstractmethod
    def call(self, interperter, arguments):
        pass

class Function(Callable):
    def __init__(self, declaration, closure):
        self.declaration = declaration
        self.closure = closure

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])

        try:
            interpreter.execute_block(self.declaration.body, environment)
        except ReturnValue as rv:
            return rv.value

        return None

    def __str__(self):
        return f'<fn {self.declaration.name.lexeme}>'
