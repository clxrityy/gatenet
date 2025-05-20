import abc

class BaseSocketServer(abc.ABC):
    """
    Abstract base class for socket servers. All socker server implementations
    (TCP, UDP, etc.) should inherit from this class and implement `start` and `stop`
    """
    def __init__(self, host="0.0.0.0", port=8000):
        """
        Initialize the server with host and port.

        :param host: The host IP address to bind to.
        :param port: The port number to listen on.
        """
        self.host = host
        self.port = port
    
    @abc.abstractmethod
    def start(self):
        """Start the server and begin handlng incoming connections or data."""
        pass
    
    @abc.abstractmethod
    def stop(self):
        """Stop the server and clean up resources."""
        pass
    