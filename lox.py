import sys

from pylox.interpreter.interpreter import Interpreter
from pylox.parser.parser import Parser
from pylox.resolver.resolver import Resolver
from pylox.scanner.scanner import Scanner

had_error = False
had_runtime_error = False
interpreter = Interpreter()

def run_prompt():
    global had_error
    while True:
        line = input('> ')
        if line is None:
            break
        run(line)
        had_error = False

def run_file(path):
    global had_error
    global had_runtime_error

    with open(path) as f:
        run(f.read())

        if had_error:
            sys.exit(65)
        if had_runtime_error:
            sys.exit(70)

def run(source):
    global had_error
    global had_runtime_error
    global interpreter

    had_error = False
    had_runtime_error = False
    interpreter.had_error = False

    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    if scanner.had_error:
        had_error = True
        return

    parser = Parser(tokens)
    statements = parser.parse()
    if parser.had_error:
        had_error = True
        return

    resolver = Resolver(interpreter)
    resolver.resolve(statements)
    if resolver.had_error:
        had_error = True
        return

    interpreter.interpret(statements)
    if interpreter.had_error:
        had_runtime_error = True

if __name__ == '__main__':
    if len(sys.argv) == 1:
        run_prompt()
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        print('Usage: lox.py [script]')
        sys.exit(64)
