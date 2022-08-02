from enum import Enum
from pylox.function.function import Callable
from pylox.interpreter.runtime_error import RuntimeError

class ClassType(Enum):
    NONE = 0
    CLASS = 1

class Class(Callable):
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods

    def arity(self):
        return 0

    def call(self, interpreter, arguments):
        instance = Instance(self)
        return instance

    def find_method(self, name):
        if name in self.methods:
            return self.methods[name]

        return None

    def __str__(self):
        return self.name

class Instance:
    def __init__(self, klass):
        self.klass = klass
        self.fields = {}

    def get(self, name):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]

        method = self.klass.find_method(name.lexeme)
        if method is not None:
            return method.bind(self)

        raise RuntimeError(name, f"Undefined property '{name.lexeme}'.")

    def set(self, name, value):
        self.fields[name.lexeme] = value

    def __str__(self):
        return self.klass.name + ' instance'
