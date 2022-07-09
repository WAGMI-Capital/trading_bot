from abc import ABC, abstractmethod
 
class Exchange(ABC):

    @abstractmethod
    def authenticate(self):
        pass

    @abstractmethod
    def go_short(self):
        pass

    @abstractmethod
    def go_long(self):
        pass