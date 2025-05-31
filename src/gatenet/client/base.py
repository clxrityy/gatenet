from abc import ABC, abstractmethod

class BaseClient(ABC):
    @abstractmethod
    def send(self, message: str, **kwargs) -> str:
        """
        Send a message to the server and return a response.
        """
        pass
    
    @abstractmethod
    def close(self):
        """
        Close the client connection.
        """
        pass