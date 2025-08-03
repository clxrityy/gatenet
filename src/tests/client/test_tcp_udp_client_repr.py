"""
Test __repr__ for TCPClient and UDPClient for coverage.
"""
from gatenet.client.tcp import TCPClient
from gatenet.client.udp import UDPClient

def test_tcpclient_repr():
    client = TCPClient(host="127.0.0.1", port=12345)
    rep = repr(client)
    assert "TCPClient" in rep
    assert "127.0.0.1" in rep
    assert "12345" in rep

def test_udpclient_repr():
    client = UDPClient(host="127.0.0.1", port=12345)
    rep = repr(client)
    assert "UDPClient" in rep
    assert "127.0.0.1" in rep
    assert "12345" in rep