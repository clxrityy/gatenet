import abc

class BaseSocketServer(abc.ABC):
    """
    Abstract base class for socket servers.

    All socket server implementations (TCP, UDP, etc.) should inherit from this class and implement `start` and `stop`.

    Example
    -------
    >>> from gatenet.socket.tcp import TCPServer
    >>> server = TCPServer(host="127.0.0.1", port=9000)
    >>> server.start()
    # Now connect with a TCP client to 127.0.0.1:9000
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8000):
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

        Example:
            >>> server = TCPServer(host="127.0.0.1", port=9000)
            >>> server.start()

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

        Example:
            >>> server = TCPServer(host="127.0.0.1", port=9000)
            >>> server.stop()

        Raises
        ------
        NotImplementedError
            If not implemented by a subclass.
        """
        pass
    