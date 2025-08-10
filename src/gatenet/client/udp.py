import socket
from gatenet.core import hooks, events
from gatenet.client.base import BaseClient

class UDPClient(BaseClient):
    """
    UDP client for sending messages to a server and receiving responses.

    Supports context manager usage for automatic resource management.

    Examples
    --------
    Basic usage::

        from gatenet.client.udp import UDPClient
        client = UDPClient(host="127.0.0.1", port=12345)
        response = client.send("ping")
        client.close()

    With context manager::

        with UDPClient(host="127.0.0.1", port=12345) as client:
            response = client.send("ping")
    """

    def __init__(self, host: str, port: int, timeout: float = 2.0):
        self.host = host
        self.port = port
        self.closed = False
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.settimeout(timeout)

    def __repr__(self):
        return f"<UDPClient host={self.host} port={self.port} closed={self.closed}>"

    def send(self, message: str, retries: int = 3, buffsize: int = 1024, **kwargs) -> str:
        """
        Send a message to the server and receive the response.

        Example:
            >>> client = UDPClient(host="127.0.0.1", port=12345)
            >>> response = client.send("ping")

        Parameters
        ----------
        message : str
            The message to send to the server.
        retries : int, optional
            Number of retries for receiving a response (default is 3).
        buffsize : int, optional
            Buffer size for receiving the response (default is 1024).
        **kwargs : dict
            Additional keyword arguments (ignored).

        Returns
        -------
        str
            The response received from the server.

        Raises
        ------
        TimeoutError
            If no response is received after the specified number of retries.
        """
        if self.closed or self._sock is None:
            raise RuntimeError("UDPClient socket is closed")
        for _ in range(retries):
            try:
                try:
                    hooks.emit(events.UDP_BEFORE_SEND, data=message)
                except Exception:
                    pass
                self._sock.sendto(message.encode(), (self.host, self.port))
                data, _ = self._sock.recvfrom(buffsize)
                decoded = data.decode()
                try:
                    hooks.emit(events.UDP_AFTER_RECV, data=decoded)
                except Exception:
                    pass
                return decoded
            except socket.timeout:
                continue
        raise TimeoutError("No response received after retries")

    def close(self):
        """
        Close the UDP client socket.

        Example:
            >>> client = UDPClient(host="127.0.0.1", port=12345)
            >>> client.close()
        """
        if hasattr(self, "_sock") and self._sock:
            self._sock.close()
            self._sock = None
        self.closed = True

    def __enter__(self):
        """
        Enter the runtime context for the UDP client.

        Example:
            >>> with UDPClient(host="127.0.0.1", port=12345) as client:
            ...     response = client.send("ping")

        Returns
        -------
        UDPClient
            The UDPClient instance.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context and close the socket.

        Example:
            >>> with UDPClient(host="127.0.0.1", port=12345) as client:
            ...     response = client.send("ping")

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
