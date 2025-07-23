"""
Edge case and error handling integration tests for gatenet TCP/UDP/HTTP client/server modules.
"""
import time
import threading
import pytest
from gatenet.socket.tcp import TCPServer
from gatenet.client.tcp import TCPClient
from gatenet.socket.udp import UDPServer
from gatenet.client.udp import UDPClient
from gatenet.http_.server import HTTPServerComponent
from gatenet.http_.client import HTTPClient
from gatenet.utils.net import get_free_port

@pytest.mark.integration
@pytest.mark.timeout(5)
def test_tcp_server_client_empty_message(tmp_path):
    """Test TCP server/client with empty message (edge case)."""
    port = get_free_port()
    server = TCPServer(host="127.0.0.1", port=port)
    server_thread = threading.Thread(target=server.start)
    server._sock.settimeout(1.0)
    server_thread.start()
    time.sleep(0.2)
    try:
        client = TCPClient(host="127.0.0.1", port=port)
        client.connect()
        with pytest.raises(TimeoutError):
            client.send("")
        client.close()
    finally:
        server.stop()
        server_thread.join(timeout=1)

@pytest.mark.integration
@pytest.mark.timeout(5)
def test_udp_server_client_empty_message(tmp_path):
    """Test UDP server/client with empty message (edge case)."""
    port = get_free_port()
    server = UDPServer(host="127.0.0.1", port=port)
    server_thread = threading.Thread(target=server.start)
    server._sock.settimeout(1.0)
    server_thread.start()
    time.sleep(0.2)
    try:
        client = UDPClient(host="127.0.0.1", port=port)
        response = client.send("")
        assert response == "Echo: "
    finally:
        server.stop()
        server_thread.join(timeout=1)

@pytest.mark.integration
@pytest.mark.timeout(5)
def test_http_server_client_invalid_route(tmp_path):
    """Test HTTP client requesting an invalid route (404 error)."""
    port = get_free_port()
    server = HTTPServerComponent(host="127.0.0.1", port=port)
    server.start()
    time.sleep(0.2)
    try:
        client = HTTPClient(f"http://127.0.0.1:{port}")
        response = client.get("/doesnotexist")  # type: ignore[attr-defined]
        assert response["ok"] is False
        assert response["status"] == 404
    finally:
        server.stop()

@pytest.mark.integration
@pytest.mark.timeout(5)
def test_tcp_server_client_timeout(tmp_path):
    """Test TCP client timeout when server does not respond."""
    port = get_free_port()
    # Do not start server
    client = TCPClient(host="127.0.0.1", port=port, timeout=0.5)
    with pytest.raises(Exception):
        client.connect()

@pytest.mark.integration
@pytest.mark.timeout(5)
def test_udp_server_client_timeout(tmp_path):
    """Test UDP client timeout when server does not respond."""
    port = get_free_port()
    # Do not start server
    client = UDPClient(host="127.0.0.1", port=port, timeout=0.5)
    with pytest.raises(Exception):
        client.send("test")
