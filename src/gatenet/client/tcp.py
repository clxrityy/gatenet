import socket
from gatenet.core import hooks, events
from gatenet.client.base import BaseClient

class TCPClient(BaseClient):
    """
    TCP client for connecting to a server, sending messages, and receiving responses.

    Supports context manager usage for automatic connection management.

    Examples
    --------
    Basic usage::

        from gatenet.client.tcp import TCPClient
        client = TCPClient(host="127.0.0.1", port=12345)
        client.connect()
        response = client.send("ping")
        client.close()

    With context manager::

        with TCPClient(host="127.0.0.1", port=12345) as client:
            response = client.send("ping")
    """

    def __init__(self, host: str, port: int, timeout: float = 5.0):
        self.host = host
        self.port = port
        self.closed = False
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(timeout)

    def __repr__(self):
        return f"<TCPClient host={self.host} port={self.port} closed={self.closed}>"

    def connect(self):
        """
        Connect to the TCP server.

        Example:
            >>> client = TCPClient(host="127.0.0.1", port=12345)
            >>> client.connect()
        """
        """
        Connect to the TCP server.

        Raises
        ------
        ConnectionError
            If the connection fails.
        """
        try:
            self._sock.connect((self.host, self.port))
        except socket.error as e:
            raise ConnectionError(f"Failed to connect: {e}")

    def send(self, message: str, buffsize: int = 1024, **kwargs) -> str:
        """
        Send a message to the server and receive the response.

        Example:
            >>> client = TCPClient(host="127.0.0.1", port=12345)
            >>> client.connect()
            >>> response = client.send("ping")
        """
        """
        Send a message to the server and receive the response.

        Parameters
        ----------
        message : str
            The message to send to the server.
        buffsize : int, optional
            The buffer size for receiving the response (default is 1024).
        **kwargs : dict
            Additional keyword arguments (ignored in TCPClient).

        Returns
        -------
        str
            The response received from the server.
        """
        # Hook: before send
        try:
            hooks.emit(events.TCP_BEFORE_SEND, data=message)
        except Exception:
            pass
        self._sock.sendall(message.encode())
        data = self._sock.recv(buffsize).decode()
        # Hook: after recv
        try:
            hooks.emit(events.TCP_AFTER_RECV, data=data)
        except Exception:
            pass
        return data

    def close(self):
        """
        Close the client connection and release resources.

        Example:
            >>> client = TCPClient(host="127.0.0.1", port=12345)
            >>> client.connect()
            >>> client.close()
        """
        """
        Close the client connection and release resources.
        """
        self._sock.close()

    def __enter__(self):
        """
        Enter the runtime context and connect to the server.

        Example:
            >>> with TCPClient(host="127.0.0.1", port=12345) as client:
            ...     response = client.send("ping")
        """
        """
        Enter the runtime context and connect to the server.

        Returns
        -------
        TCPClient
            The connected TCPClient instance.
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context and close the connection.

        Example:
            >>> with TCPClient(host="127.0.0.1", port=12345) as client:
            ...     response = client.send("ping")
        """
        """
        Exit the runtime context and close the connection.

        Parameters
        ----------
        exc_type : type
            Exception type (if any).
        exc_val : Exception
            Exception value (if any).
        exc_tb : traceback
            Exception traceback (if any).
        """
        self.close()