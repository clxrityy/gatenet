"""
Test BaseClient ABC for coverage.
"""
import pytest
from gatenet.client.base import BaseClient

class DummyClient(BaseClient):
    def __init__(self):
        self.closed = False
    def send(self, message: str, **kwargs) -> str:
        return f"echo:{message}"
    def close(self):
        self.closed = True
    def __repr__(self):
        return f"<BaseClient DummyClient at {hex(id(self))}>"

def test_baseclient_init():
    client = DummyClient()
    assert isinstance(client, BaseClient)

def test_baseclient_send():
    client = DummyClient()
    result = client.send("hello")
    assert result == "echo:hello"

def test_baseclient_close():
    client = DummyClient()
    client.closed = False
    client.close()
    assert client.closed

def test_baseclient_repr():
    client = DummyClient()
    rep = repr(client)
    assert "BaseClient" in rep
