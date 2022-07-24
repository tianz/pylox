from pylox.interpreter.runtime_error import RuntimeError

class Environment:
    def __init__(self):
        self.values = {}

    def define(self, name, value):
        self.values[name] = value

    def assign(self, token, value):
        if token.lexeme in self.values:
            self.values[token.lexeme] = value
            return

        raise RuntimeError(token, f"Undefined variable '{token.lexeme}'.")

    def get(self, token):
        if token.lexeme in self.values:
            return self.values[token.lexeme]
        raise RuntimeError(token, f"Undefined variable '{token.lexeme}'.")
