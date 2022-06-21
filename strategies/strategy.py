from abc import ABC, abstractmethod
 
class Strategy(ABC):
 
    @abstractmethod
    def _get_market_data(self):
        pass
    
    @abstractmethod
    def _populate_indicators(self):
        pass
    
    @abstractmethod
    def crunch_data(self):
        pass
    
    @abstractmethod
    def should_long(self):
        pass
    
    @abstractmethod
    def should_short(self):
        pass

    @abstractmethod
    def _long_filters(self):
        pass
    
    @abstractmethod
    def _short_filters(self):
        pass