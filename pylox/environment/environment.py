from pylox.interpreter.runtime_error import RuntimeError

class Environment:
    def __init__(self):
        self.values = {}

    def define(self, name, value):
        self.values[name] = value

    def get(self, token):
        if token.lexeme in self.values:
            return self.values[token.lexeme]
        raise RuntimeError(token, f"Undefined variable '{token.lexeme}'.")
