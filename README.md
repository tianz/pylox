# pylox

A tree-walk interpreter of the Lox programming language, implemented in Python.

Lox is a tiny programming language described in the book [Crafting Interpreters][craftinginterpreters]. The tree-walk interpreter was originally implemented in Java by the author.

## Usage
### REPL mode
```
python lox.py
```

### Run file
```
python lox.py [script]
```

## Test
```
python -m unittest discover test
```

<!-- Reference Links -->
[craftinginterpreters]: https://github.com/munificent/craftinginterpreters
