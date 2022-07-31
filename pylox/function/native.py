import time

from .function import Callable

class Clock(Callable):
    def arity(self):
        return 0

    def call(self, interpreter, arguments):
        return int(time.time())

    def __str__(self):
        return '<native fn>'
