"""
Test BaseSocketServer ABC for coverage.
"""
import pytest
from gatenet.socket.base import BaseSocketServer

class DummySocketServer(BaseSocketServer):
    def __init__(self, host="127.0.0.1", port=8000):
        super().__init__(host, port)
        self._started = False
    def start(self):
        self._started = True
    def stop(self):
        self._started = False
    def __repr__(self):
        return f"<BaseSocketServer DummySocketServer host={self.host} port={self.port} started={self._started}>"

def test_basesocketserver_init():
    server = DummySocketServer(host="127.0.0.1", port=9999)
    assert server.host == "127.0.0.1"
    assert server.port == 9999
    assert not server._started

def test_basesocketserver_start_stop():
    server = DummySocketServer()
    server.start()
    assert server._started
    server.stop()
    assert not server._started

def test_basesocketserver_repr():
    server = DummySocketServer(host="1.2.3.4", port=1234)
    rep = repr(server)
    assert "BaseSocketServer" in rep
    assert "1.2.3.4" in rep
    assert "1234" in rep
