from abc import ABC, abstractmethod

class BaseClient(ABC):
    """
    Abstract base class for network clients.

    All client implementations must provide methods to send messages and close the connection.

    Examples
    --------
    Subclassing::

        class MyClient(BaseClient):
            def send(self, message: str, **kwargs) -> str:
                return "response"
            def close(self):
                pass

    Usage::

        client = MyClient()
        response = client.send("hello")
        client.close()
    """

    @abstractmethod
    def send(self, message: str, **kwargs) -> str:
        """
        Send a message to the server and return a response.

        Example:
            >>> class MyClient(BaseClient):
            ...     def send(self, message: str, **kwargs) -> str:
            ...         return "response"
            ...     def close(self):
            ...         pass
            >>> client = MyClient()
            >>> response = client.send("hello")

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

        Example:
            >>> client = MyClient()
            >>> client.close()

        This should release any resources and close the underlying socket or connection.
        """
        pass