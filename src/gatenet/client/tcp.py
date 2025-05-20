import socket

class TCPClient:
    """
    A basic TCP client that connects to a server, sends a message,
    and receives a response.
    """
    def __init__(self, host: str, port: int):
        """
        Initialize the TCP client.

        :param host: The server's host IP address.
        :param port: The server's port number.
        """
        self.host = host
        self.port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        """
        Connect to the TCP server.
        """
        self._sock.connect((self.host, self.port))
        
    def send(self, message: str):
        """
        Send a message and receive the server response
        """
        self._sock.sendall(message.encode())
        return self._sock.recv(1024).decode()
    
    def close(self):
        """
        Close the client connection.
        """
        self._sock.close()