from abc import ABC, abstractmethod

class BaseClient(ABC):
    """
    Abstract base class for network clients.

    All client implementations must provide methods to send messages and close the connection.
    """

    @abstractmethod
    def send(self, message: str, **kwargs) -> str:
        """
        Send a message to the server and return a response.

        Parameters
        ----------
        message : str
            The message to send to the server.
        **kwargs : dict
            Additional keyword arguments for protocol-specific options.

        Returns
        -------
        str
            The response received from the server.
        """
        pass

    @abstractmethod
    def close(self):
        """
        Close the client connection.

        This should release any resources and close the underlying socket or connection.
        """
        pass