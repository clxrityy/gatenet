"""
test_netinfo.py — Tests for network interface and WiFi scanning utilities in gatenet.utils.netinfo.
"""
import pytest
from gatenet.utils import netinfo


def test_list_network_interfaces(monkeypatch):
    # Mock psutil if available
    class MockAddr:
        def __init__(self, family, address):
            self.family = family
            self.address = address
    class MockPsutil:
        AF_LINK = 17
        @staticmethod
        def net_if_addrs():
            return {
                "eth0": [
                    MockAddr(family=2, address="192.168.1.10"),
                    MockAddr(family=17, address="aa:bb:cc:dd:ee:ff"),
                ],
                "lo": [
                    MockAddr(family=2, address="127.0.0.1"),
                ],
            }
    monkeypatch.setattr(netinfo, "psutil", MockPsutil)
    interfaces = netinfo.list_network_interfaces()
    assert any(i["name"] == "eth0" and i["ip"] == "192.168.1.10" and i["mac"] == "aa:bb:cc:dd:ee:ff" for i in interfaces)
    assert any(i["name"] == "lo" and i["ip"] == "127.0.0.1" for i in interfaces)


def test_scan_wifi_networks_macos(monkeypatch):
    # Simulate macOS
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(netinfo, "_scan_wifi_macos", lambda: [{"ssid": "TestWiFi", "signal": "-40", "security": "WPA2"}])
    result = netinfo.scan_wifi_networks()
    assert result == [{"ssid": "TestWiFi", "signal": "-40", "security": "WPA2"}]


def test_scan_wifi_networks_linux(monkeypatch):
    # Simulate Linux
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(netinfo, "_scan_wifi_linux", lambda iface: [{"ssid": "LinuxWiFi", "signal": "-50", "security": "WPA3"}])
    result = netinfo.scan_wifi_networks("wlan0")
    assert result == [{"ssid": "LinuxWiFi", "signal": "-50", "security": "WPA3"}]


def test_scan_wifi_networks_unsupported(monkeypatch):
    monkeypatch.setattr("platform.system", lambda: "Windows")
    result = netinfo.scan_wifi_networks()
    assert result == [{"error": "WiFi scan not supported on this OS"}]


def test__parse_linux_iwlist_output():
    sample = """
Cell 01 - Address: 00:11:22:33:44:55\n                    ESSID:"LinuxWiFi"\n                    Signal level=-50 dBm\n                    Encryption key:on\n"""
    out = netinfo._parse_linux_iwlist_output(sample)
    assert out == [{"ssid": "LinuxWiFi", "signal": "-50", "security": "WPA/WEP"}]


def test__scan_wifi_macos_error(monkeypatch):
    def raise_exc(*a, **k):
        raise RuntimeError("fail")
    monkeypatch.setattr("subprocess.check_output", raise_exc)
    out = netinfo._scan_wifi_macos()
    assert out == [{"error": "fail"}]


def test__scan_wifi_linux_error(monkeypatch):
    def raise_exc2(*a, **k):
        raise RuntimeError("fail2")
    monkeypatch.setattr("subprocess.check_output", raise_exc2)
    out = netinfo._scan_wifi_linux("wlan0")
    assert out == [{"error": "fail2"}]
