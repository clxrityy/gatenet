import socket
from gatenet.client.base import BaseClient

class UDPClient(BaseClient):
    """
    A basic UDP client that sends a message to a server and waits for a response.
    """
    def __init__(self, host: str, port: int, timeout: float = 2.0):
        """
        Initialize the UDP client.

        :param host: The server's host IP address.
        :param port: The server's port number.
        """
        self.host = host
        self.port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.settimeout(timeout)  # Set a timeout for receiving data

    def send(self, message: str, retries: int = 3, buffsize: int = 1024):
        """
        Send a message and receive the server response.
        
        :param message: The message to send to the server.
        :param retries: The number of retries for receiving a response.
        :param buffsize: The buffer size for receiving the response.
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
        Close the client socket.
        """
        self._sock.close()
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
