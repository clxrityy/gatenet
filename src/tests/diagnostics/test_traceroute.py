import pytest
from unittest.mock import patch
import socket
from gatenet.diagnostics.traceroute import traceroute

def test_traceroute_resolves_host(monkeypatch):
    """Test that traceroute resolves the host and returns hops."""
    monkeypatch.setattr("socket.gethostbyname", lambda host: "1.2.3.4")

    class DummySocket:
        def __init__(self, *a, **kw):
            self.timeout = None
            self.closed = False
            self.ttl = None
            self.bound = False
            self.sent = False
            self.recv_count = 0

        def setsockopt(self, *a, **kw):
            self.ttl = a[-1]

        def settimeout(self, timeout):
            self.timeout = timeout

        def bind(self, addr):
            self.bound = True

        def sendto(self, data, addr):
            self.sent = True

        def recvfrom(self, bufsize):
            # Simulate a direct route: destination IP on first hop
            self.recv_count += 1
            if self.recv_count == 1:
                return (b"", ("1.2.3.4", 0))
            return (b"", (f"10.0.0.{self.recv_count}", 0))

        def close(self):
            self.closed = True

    monkeypatch.setattr("socket.socket", lambda *a, **kw: DummySocket())
    monkeypatch.setattr("socket.gethostbyaddr", lambda ip: (f"host-{ip}", [], [ip]))

    hops = traceroute("example.com", max_hops=3, timeout=0.1)

    # Should return 1 hop, which is the destination
    assert len(hops) == 1
    assert hops[-1][1] == "1.2.3.4"
    assert all(isinstance(h[0], int) for h in hops)
    assert all(isinstance(h[1], str) for h in hops)

def test_traceroute_unresolvable_host():
    """Test that traceroute raises ValueError for unresolvable host."""
    with patch("socket.gethostbyname", side_effect=socket.gaierror):
        with pytest.raises(ValueError):
            traceroute("notarealhost.local")

def test_traceroute_timeout(monkeypatch):
    """Test that traceroute handles timeouts gracefully."""
    monkeypatch.setattr("socket.gethostbyname", lambda host: "1.2.3.4")

    class TimeoutSocket:
        def __init__(self, *a, **kw):
            # This constructor is intentionally left empty because
            # the TimeoutSocket does not need to initialize any state for this test.
            pass
        def setsockopt(self, *a, **kw):
            # This method is intentionally left empty because
            # the TimeoutSocket does not need to set any socket options for this test.
            pass
        def settimeout(self, timeout):
            # This method is intentionally left empty because
            # the TimeoutSocket does not need to set a timeout for this test.
            pass
        def bind(self, addr):
            # This method is intentionally left empty because
            # the TimeoutSocket does not need to bind to any address for this test.
            pass
        def sendto(self, data, addr):
            # This method is intentionally left empty because
            # the TimeoutSocket does not need to actually send any data for this test.
            pass
        def recvfrom(self, bufsize): raise TimeoutError()
        def close(self):
            # This method is intentionally left empty because
            # the TimeoutSocket does not need to close any resources for this test.
            pass

    monkeypatch.setattr("socket.socket", lambda *a, **kw: TimeoutSocket())
    monkeypatch.setattr("socket.gethostbyaddr", lambda ip: ("", [], [ip]))

    hops = traceroute("example.com", max_hops=2, timeout=0.01)
    assert len(hops) == 2
    assert all(h[1] == "*" for h in hops)
    assert all(h[2] is None for h in hops)