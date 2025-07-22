import socket
from gatenet.client.base import BaseClient

class UDPClient(BaseClient):
    """
    UDP client for sending messages to a server and receiving responses.

    Supports context manager usage for automatic resource management.
    """

    def __init__(self, host: str, port: int, timeout: float = 2.0):
        """
        Initialize the UDP client.

        Parameters
        ----------
        host : str
            The server's host IP address.
        port : int
            The server's port number.
        timeout : float, optional
            Timeout for receiving data in seconds (default is 2.0).
        """
        self.host = host
        self.port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.settimeout(timeout)

    def send(self, message: str, retries: int = 3, buffsize: int = 1024, **kwargs) -> str:
        """
        Send a message to the server and receive the response.

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
        for _ in range(retries):
            try:
                self._sock.sendto(message.encode(), (self.host, self.port))
                data, _ = self._sock.recvfrom(buffsize)
                return data.decode()
            except socket.timeout:
                continue
        raise TimeoutError(f"Failed to receive response after {retries} retries.")

    def close(self):
        """
        Close the client socket and release resources.
        """
        self._sock.close()

    def __enter__(self):
        """
        Enter the runtime context for the UDP client.

        Returns
        -------
        UDPClient
            The UDPClient instance.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context and close the socket.

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
