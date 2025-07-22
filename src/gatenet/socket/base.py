import abc

class BaseSocketServer(abc.ABC):
    """
    Abstract base class for socket servers.

    All socket server implementations (TCP, UDP, etc.) should inherit from this class and implement `start` and `stop`.
    """

    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        """
        Initialize the server with host and port.

        Parameters
        ----------
        host : str, optional
            The host IP address to bind to (default is "0.0.0.0").
        port : int, optional
            The port number to listen on (default is 8000).
        """
        self.host = host
        self.port = port

    @abc.abstractmethod
    def start(self):
        """
        Start the server and begin handling incoming connections or data.

        Raises
        ------
        NotImplementedError
            If not implemented by a subclass.
        """
        pass

    @abc.abstractmethod
    def stop(self):
        """
        Stop the server and clean up resources.

        Raises
        ------
        NotImplementedError
            If not implemented by a subclass.
        """
        pass
    