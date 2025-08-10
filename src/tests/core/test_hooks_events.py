from gatenet.core import hooks, events
from gatenet.discovery.ssh import _identify_service
from gatenet.diagnostics import ping
from gatenet.client import UDPClient
from gatenet.socket import UDPServer
from gatenet.client import TCPClient
from gatenet.socket import TCPServer
from gatenet.utils import get_free_port
import threading
import time
import shutil
import pytest


def test_discovery_hooks_emitted():
    seen = {}
    def before(port, banner):
        seen['before'] = (port, banner)
    def after(port, banner, result):
        seen['after'] = (port, banner, result)

    hooks.on(events.DISCOVERY_BEFORE_DETECT, before)
    hooks.on(events.DISCOVERY_AFTER_DETECT, after)
    try:
        res = _identify_service(22, "SSH-2.0-OpenSSH_8.9p1")
        assert res.startswith("OpenSSH")
        assert seen.get('before') == (22, "ssh-2.0-openssh_8.9p1")
        assert 'after' in seen and seen['after'][2].startswith("OpenSSH")
    finally:
        hooks.clear(events.DISCOVERY_BEFORE_DETECT)
        hooks.clear(events.DISCOVERY_AFTER_DETECT)


def test_udp_client_hooks_emitted():
    seen = {"before": [], "after": []}
    hooks.on(events.UDP_BEFORE_SEND, lambda data: seen["before"].append(data))
    hooks.on(events.UDP_AFTER_RECV, lambda data: seen["after"].append(data))

    server = UDPServer("127.0.0.1", 9310)
    t = threading.Thread(target=server.start, daemon=True)
    t.start()
    time.sleep(0.3)

    try:
        client = UDPClient("127.0.0.1", 9310)
        resp = client.send("ping")
        client.close()
        assert resp.startswith("Echo:")
        assert seen["before"] == ["ping"]
        assert len(seen["after"]) == 1 and seen["after"][0].startswith("Echo:")
    finally:
        server.stop()
        hooks.clear(events.UDP_BEFORE_SEND)
        hooks.clear(events.UDP_AFTER_RECV)


def test_tcp_client_hooks_emitted():
    seen = {"before": [], "after": []}
    hooks.on(events.TCP_BEFORE_SEND, lambda data: seen["before"].append(data))
    hooks.on(events.TCP_AFTER_RECV, lambda data: seen["after"].append(data))

    port = get_free_port()
    server = TCPServer("127.0.0.1", port)
    t = threading.Thread(target=server.start, daemon=True)
    t.start()
    time.sleep(0.3)

    try:
        client = TCPClient("127.0.0.1", port)
        client.connect()
        resp = client.send("ping")
        client.close()
        assert resp.startswith("Echo:")
        assert seen["before"] == ["ping"]
        assert len(seen["after"]) == 1 and seen["after"][0].startswith("Echo:")
    finally:
        server.stop()
        hooks.clear(events.TCP_BEFORE_SEND)
        hooks.clear(events.TCP_AFTER_RECV)


@pytest.mark.skipif(shutil.which("ping") is None, reason="ping not available in environment")
def test_ping_hooks_emitted():
    seen = {}
    hooks.on(events.PING_BEFORE, lambda host, count: seen.setdefault('before', []).append((host, count)))
    hooks.on(events.PING_AFTER, lambda host, result: seen.setdefault('after', []).append((host, result)))
    try:
        ping("1.1.1.1", count=1)
        assert 'before' in seen and seen['before'][0][0] == "1.1.1.1"
        assert 'after' in seen and seen['after'][0][0] == "1.1.1.1"
        assert isinstance(seen['after'][0][1], dict)
    finally:
        hooks.clear(events.PING_BEFORE)
        hooks.clear(events.PING_AFTER)
