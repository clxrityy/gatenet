import socket
from gatenet.socket.base import BaseSocketServer

class UDPServer(BaseSocketServer):
    """
    UDP server that listens for datagrams and echoes them back with an 'Echo: ' prefix.
    """

    def __init__(self, host: str = "0.0.0.0", port: int = 8001):
        """
        Initialize the UDP server.

        Parameters
        ----------
        host : str, optional
            The host IP address to bind to (default is "0.0.0.0").
        port : int, optional
            The port number to listen on (default is 8001).
        """
        super().__init__(host, port)
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        """
        Start the UDP server and listen for incoming datagrams.

        Raises
        ------
        OSError
            If the socket is closed externally or binding fails.
        """
        self._sock.bind((self.host, self.port))
        print(f"[UDPServer] Listening on {self.host}:{self.port}")

        try:
            while True:
                try:
                    data, addr = self._sock.recvfrom(1024)
                    print(f"[UDPServer] Received from {addr}: {data.decode()}")
                    self._sock.sendto(b"Echo: " + data, addr)
                except socket.timeout:
                    continue
        except OSError:
            # Socket closed externally - expected on shutdown
            pass
        finally:
            self.stop()

    def stop(self):
        """
        Stop the UDP server and close the socket.

        This method closes the server socket and prints a shutdown message.
        """
        self._sock.close()
        print("[UDPServer] Server stopped")