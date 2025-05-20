import socket
import threading
import time
import pytest
from gatenet.socket_server.udp import UDPServer

@pytest.fixture
def udp_server():
    """
    Fixture to create and start a UDP server for testing.
    """
    server = UDPServer(host="127.0.0.1", port=9091)
    thread = threading.Thread(target=server.start, daemon=True)
    thread.start()
    time.sleep(0.1)
    yield
    server.stop()
    time.sleep(0.1)
    
def test_udp_echo(udp_server):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    test_message = b"ping"
    client.sendto(test_message, ("127.0.0.1", 9091))
    data, _ = client.recvfrom(1024)
    assert data == b"Echo: " + test_message
    client.close()
