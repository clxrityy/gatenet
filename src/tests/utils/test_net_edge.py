"""
Edge case tests for get_free_port.
"""
import pytest
from gatenet.utils.net import get_free_port

def test_get_free_port_type():
    port = get_free_port()
    assert isinstance(port, int)
    assert 1024 < port < 65535

def test_get_free_port_multiple():
    ports = [get_free_port() for _ in range(5)]
    assert len(set(ports)) == 5
