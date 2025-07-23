"""
Integration tests for gatenet: TCP and UDP client/server end-to-end communication.

Covers TCP and UDP echo, error handling, and edge cases.
"""

import time
import threading
import pytest
from gatenet.socket.tcp import TCPServer
from gatenet.client.tcp import TCPClient
from gatenet.socket.udp import UDPServer
from gatenet.client.udp import UDPClient
from gatenet.utils.net import get_free_port

@pytest.mark.integration
@pytest.mark.timeout(5)
def test_tcp_server_client_echo(tmp_path):
    """Test TCP server and client integration with echo and error handling."""
    port = get_free_port()
    server = TCPServer(host="127.0.0.1", port=port)

    server_thread = None
    try:
        # Patch server socket to have a timeout so it doesn't block forever
        server._sock.settimeout(1.0)
        server_thread = threading.Thread(target=server.start, daemon=True)
        server_thread.start()
        time.sleep(0.2)

        client = TCPClient(host="127.0.0.1", port=port)
        client.connect()
        response = client.send("hello")
        assert response == "Echo: hello"
        client.close()
    finally:
        server.stop()
        if server_thread:
            server_thread.join(timeout=1)

@pytest.mark.integration
@pytest.mark.timeout(5)
def test_udp_server_client_echo(tmp_path):
    """Test UDP server and client integration with echo and error handling."""
    port = get_free_port()
    server = UDPServer(host="127.0.0.1", port=port)

    server_thread = None
    try:
        server._sock.settimeout(1.0)
        server_thread = threading.Thread(target=server.start, daemon=True)
        server_thread.start()
        time.sleep(0.2)

        client = UDPClient(host="127.0.0.1", port=port)
        response = client.send("hello")
        assert response == "Echo: hello"
    finally:
        server.stop()
        if server_thread:
            server_thread.join(timeout=1)

@pytest.mark.integration
@pytest.mark.timeout(3)
def test_tcp_server_client_connection_refused(tmp_path):
    """Test TCP client connection refused edge case."""
    port = get_free_port()
    client = TCPClient(host="127.0.0.1", port=port)
    with pytest.raises(Exception):
        client.connect()
