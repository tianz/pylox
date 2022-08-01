from pylox.function.function import Callable

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

    def __str__(self):
        return self.klass.name + ' instance'