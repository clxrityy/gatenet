import socket
import threading
import time
import pytest
from gatenet.socket.tcp import TCPServer

@pytest.fixture
def tcp_server():
    """
    Fixture to create and start a TCP server for testing.
    """
    server = TCPServer(host="127.0.0.1", port=9090)
    thread = threading.Thread(target=server.start, daemon=True)
    thread.start()
    time.sleep(0.1) # Give the server time to start
    yield
    server.stop()
    time.sleep(0.1) # Give the server time to stop
    
def test_tcp_echo(tcp_server):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9090))
    test_message = b"hello"
    client.sendall(test_message)
    response = client.recv(1024)
    assert response == b"Echo: " + test_message
    client.close()