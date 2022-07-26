from abc import ABC, abstractmethod

class Callable(ABC):
    @abstractmethod
    def arity(self):
        pass

    @abstractmethod
    def call(self, interperter, arguments):
        pass
