import socket
from gatenet.client.base import BaseClient

class TCPClient(BaseClient):
    """
    A basic TCP client that connects to a server, sends a message,
    and receives a response.
    """
    def __init__(self, host: str, port: int, timeout: float = 5.0):
        """
        Initialize the TCP client.

        :param host: The server's host IP address.
        :param port: The server's port number.
        :param timeout: The timeout for the connection in seconds.
        """
        self.host = host
        self.port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.settimeout(timeout)
    
    def connect(self):
        """
        Connect to the TCP server.
        """
        try:
            self._sock.connect((self.host, self.port))
        except socket.error as e:
            raise ConnectionError(f"Failed to connect: {e}")
        
    def send(self, message: str, buffsize: int = 1024):
        """
        Send a message and receive the server response
        """
        self._sock.sendall(message.encode())
        return self._sock.recv(buffsize).decode()
    
    def close(self):
        """
        Close the client connection.
        """
        self._sock.close()
        
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()