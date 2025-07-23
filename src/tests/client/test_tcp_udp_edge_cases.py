import pytest
import socket
import threading
import time
from gatenet.socket import TCPServer, UDPServer
from gatenet.client import TCPClient, UDPClient
from gatenet.utils.net import get_free_port

def test_tcp_connection_refused():
    port = get_free_port()
    client = TCPClient("127.0.0.1", port)
    with pytest.raises(ConnectionError):
        client.connect()

def test_udp_no_server_timeout():
    port = get_free_port()
    client = UDPClient("127.0.0.1", port, timeout=0.2)
    with pytest.raises(TimeoutError):
        client.send("no server")

def test_tcp_send_empty_message():
    port = get_free_port()
    server = TCPServer("127.0.0.1", port)
    thread = threading.Thread(target=server.start, daemon=True)
    thread.start()
    time.sleep(0.2)
    client = TCPClient("127.0.0.1", port)
    client.connect()
    with pytest.raises(TimeoutError):
        client.send("")
    client.close()
    server.stop()

def test_udp_send_empty_message():
    port = get_free_port()
    server = UDPServer("127.0.0.1", port)
    thread = threading.Thread(target=server.start, daemon=True)
    thread.start()
    time.sleep(0.2)
    client = UDPClient("127.0.0.1", port, timeout=0.2)
    response = client.send("")
    assert response == "Echo: "
    server.stop()

def test_tcp_abrupt_server_disconnect():
    port = get_free_port()
    server = TCPServer("127.0.0.1", port)
    thread = threading.Thread(target=server.start, daemon=True)
    thread.start()
    time.sleep(0.2)
    client = TCPClient("127.0.0.1", port)
    client.connect()
    server.stop()
    time.sleep(0.1)
    try:
        resp = client.send("test after stop")
        assert resp in ["", None, "Echo: test after stop"]
    except OSError:
        pass
    client.close()

def test_udp_invalid_address():
    client = UDPClient("256.256.256.256", 12345, timeout=0.2)
    with pytest.raises(Exception):
        client.send("test")
