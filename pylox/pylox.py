import sys

had_error = False;

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
    print(source)

def error(line, message):
    report(line, '', message)

def report(line, where, message):
    print(f'[line {line}] Error{where}: {message}')
    had_error = True;

if __name__ == '__main__':
    if len(sys.argv) == 1:
        run_prompt()
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        print('Usage: jlox [script]')
        sys.exit(64)
