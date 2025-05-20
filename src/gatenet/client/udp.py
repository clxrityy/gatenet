import socket

class UDPClient:
    """
    A basic UDP client that sends a message to a server and waits for a response.
    """
    def __init__(self, host: str, port: int):
        """
        Initialize the UDP client.

        :param host: The server's host IP address.
        :param port: The server's port number.
        """
        self.host = host
        self.port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.settimeout(2.0)  # Set a timeout for receiving data
        
    def send(self, message: str):
        """
        Send a message and receive the server response.
        
        :param message: The message to send to the server.
        """
        self._sock.sendto(message.encode(), (self.host, self.port))
        data, _ = self._sock.recvfrom(1024)
        return data.decode()
    
    def close(self):
        """
        Close the client socket.
        """
        self._sock.close()