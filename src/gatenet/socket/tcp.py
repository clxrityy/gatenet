import socket
import threading
from gatenet.socket.base import BaseSocketServer

class TCPServer(BaseSocketServer):
    """
    A simple multithreaded TCP server that accepts incoming connections and
    echoes back any data it receives, prefixed with 'Echo: '.
    """
    def __init__(self, host: str = "0.0.0.0", port: int = 8000):
        """
        Initialize the TCP server
        
        :param host: The host IP address to bind to.
        :param port: The port number to listen on.
        """
        super().__init__(host, port)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._is_running = False
        
    def start(self):
        """
        Start the TCP server. Accepts connections and spawns a new thread
        for each client to handle communication.
        """
        self._sock.bind((self.host, self.port))
        self._sock.listen()
        self._is_running = True
        print(f"[TCPServer] Listening on {self.host}:{self.port}")
        
        try:
            while self._is_running:
                try:
                    client, addr = self._sock.accept()
                    thread = threading.Thread(
                        target=self._handle_client,
                        args=(client, addr),
                        daemon=True
                    )
                    thread.start()
                except socket.timeout:
                    continue # Re-check is_running flag
        except OSError:
            # Socket closed externally - expected on shutdown
            pass
        finally:
            self.stop()
        
            
    def _handle_client(self, client_socket: socket.socket, addr: tuple):
        """
        Handle a connected TCP client.

        :param client_socket: The socket connected to the client.
        :param addr: Address of the connected client.
        """
        with client_socket:
            print(f"[TCPServer] Accepted connection from {addr}")
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break # Connection closed
                client_socket.sendall(b"Echo: " + data)
    
    def stop(self):
        """
        Stop the TCP server and release the socket.
        """
        self._is_running = False
        self._sock.close()
        print("[TCPServer] Server stopped.")