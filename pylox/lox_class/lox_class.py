from pylox.function.function import Callable
from pylox.interpreter.runtime_error import RuntimeError

class Class(Callable):
    def __init__(self, name):
        self.name = name

    def arity(self):
        return 0

    def call(self, interpreter, arguments):
        instance = Instance(self)
        return instance

    def __str__(self):
        return self.name

class Instance:
    def __init__(self, klass):
        self.klass = klass
        self.fields = {}

    def get(self, name):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]

        raise RuntimeError(name, f"Undefined property '{name.lexeme}'.")

    def set(self, name, value):
        self.fields[name.lexeme] = value

    def __str__(self):
        return self.klass.name + ' instance'
