import sys

from pylox.scanner.scanner import Scanner

def run_prompt():
    while True:
        line = input('> ')
        if line is None:
            break
        run(line)

def run_file(path):
    with open(path) as f:
        run(f.read())

def run(source):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    if scanner.had_error:
        sys.exit(65)

    for token in tokens:
        print(token)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        run_prompt()
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        print('Usage: jlox [script]')
        sys.exit(64)
