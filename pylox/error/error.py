from pylox.scanner.token import TokenType

def line_error(line, message):
    report(line, '', message)

def token_error(token, message):
    if token.type == TokenType.EOF:
        report(token.line, 'at end', message)
    else:
        report(token.line, f"at '{token.lexeme}'", message)

def report(line, where, message):
    print(f'[line {line}] Error {where}: {message}')
