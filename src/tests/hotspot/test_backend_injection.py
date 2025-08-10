import pytest

from gatenet.hotspot import Hotspot, HotspotConfig, HotspotBackend, BackendResult


class DummyBackend(HotspotBackend):
    def __init__(self):
        self.started = False

    def start(self) -> BackendResult:
        self.started = True
        return BackendResult(ok=True)

    def stop(self) -> BackendResult:
        self.started = False
        return BackendResult(ok=True)

    def devices(self):
        if self.started:
            return [{"ip": "192.168.4.2", "mac": "aa:bb:cc:dd:ee:ff", "hostname": "test-device"}]
        return []


def test_hotspot_uses_injected_backend_for_start_stop_and_devices():
    backend = DummyBackend()
    cfg = HotspotConfig(ssid="X", password="Y")
    hs = Hotspot(cfg, backend=backend)

    assert not hs.is_running
    assert backend.started is False

    assert hs.start() is True
    assert hs.is_running is True
    assert backend.started is True

    devices = hs.get_connected_devices()
    assert devices and devices[0]["ip"] == "192.168.4.2"

    assert hs.stop() is True
    assert hs.is_running is False
    assert backend.started is False
