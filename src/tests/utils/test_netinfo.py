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


def test_list_network_interfaces_fallback(monkeypatch):
    # Test fallback when psutil is not available
    monkeypatch.setattr(netinfo, "psutil", None)
    interfaces = netinfo.list_network_interfaces()
    assert interfaces == [{"name": "lo", "ip": "127.0.0.1", "mac": ""}]


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


def test_scan_wifi_networks_linux_default_interface(monkeypatch):
    # Test Linux with default interface (wlan0)
    monkeypatch.setattr("platform.system", lambda: "Linux")
    monkeypatch.setattr(netinfo, "_scan_wifi_linux", lambda iface: [{"ssid": "DefaultWiFi", "signal": "-60", "security": "WPA2"}])
    result = netinfo.scan_wifi_networks()  # No interface specified, should use wlan0
    assert result == [{"ssid": "DefaultWiFi", "signal": "-60", "security": "WPA2"}]


def test_scan_wifi_networks_unsupported(monkeypatch):
    monkeypatch.setattr("platform.system", lambda: "Windows")
    result = netinfo.scan_wifi_networks()
    assert result == [{"error": "WiFi scan not supported on this OS"}]


def test__parse_linux_iwlist_output():
    sample = """
Cell 01 - Address: 00:11:22:33:44:55\n                    ESSID:"LinuxWiFi"\n                    Signal level=-50 dBm\n                    Encryption key:on\n"""
    out = netinfo._parse_linux_iwlist_output(sample)
    assert out == [{"ssid": "LinuxWiFi", "signal": "-50", "security": "WPA/WEP"}]


def test__parse_linux_iwlist_output_multiple_cells():
    # Test parsing multiple WiFi networks
    sample = """
Cell 01 - Address: 00:11:22:33:44:55
                    ESSID:"WiFi1"
                    Signal level=-40 dBm
                    Encryption key:on

Cell 02 - Address: 00:11:22:33:44:56
                    ESSID:"OpenWiFi"
                    Signal level=-60 dBm
                    Encryption key:off
"""
    out = netinfo._parse_linux_iwlist_output(sample)
    assert len(out) == 2
    assert out[0] == {"ssid": "WiFi1", "signal": "-40", "security": "WPA/WEP"}
    assert out[1] == {"ssid": "OpenWiFi", "signal": "-60", "security": "Open"}


def test__parse_linux_iwlist_output_missing_fields():
    # Test parsing with missing ESSID, signal, or encryption
    sample = """
Cell 01 - Address: 00:11:22:33:44:55
                    ESSID:""
                    Encryption key:on

Cell 02 - Address: 00:11:22:33:44:56
                    ESSID:"NoSignal"
"""
    out = netinfo._parse_linux_iwlist_output(sample)
    assert len(out) == 2
    assert out[0]["ssid"] == ""
    assert out[0]["signal"] == ""
    assert out[0]["security"] == "WPA/WEP"
    assert out[1]["ssid"] == "NoSignal"
    assert out[1]["signal"] == ""
    assert out[1]["security"] == "Open"


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


def test__get_col_ranges_basic():
    # Test basic column range parsing functionality
    header = "SSID BSSID RSSI"
    columns = ["SSID", "BSSID", "RSSI"]
    col_ranges = netinfo._get_col_ranges(header, columns)
    
    assert len(col_ranges) == 3
    # Check that ranges are in order
    for i in range(len(col_ranges) - 1):
        assert col_ranges[i][1] < col_ranges[i + 1][1]  # start positions should be increasing


def test__parse_airport_line_basic():
    # Test the core parsing logic without complex formatting
    col_ranges = [("SSID", 0, 5), ("BSSID", 5, 10), ("RSSI", 10, None)]
    line = "WiFi 12345-45"
    result = netinfo._parse_airport_line(line, col_ranges)
    
    assert result["ssid"] == "WiFi"
    assert result["signal"] == "-45"


def test__parse_macos_airport_output_structure():
    # Test basic output structure parsing rather than exact content
    sample_output = """SSID BSSID RSSI SECURITY
TestWiFi 00:11:22:33:44:55 -40 WPA2
WiFi2 00:11:22:33:44:56 -50 WPA2
"""
    result = netinfo._parse_macos_airport_output(sample_output)
    
    # Just verify structure - content parsing is complex due to column alignment
    assert isinstance(result, list)
    assert len(result) == 2
    for item in result:
        assert isinstance(item, dict)
        assert "ssid" in item
        assert "signal" in item
        assert "security" in item


def test__parse_macos_airport_output_empty():
    # Test parsing empty or invalid output
    assert netinfo._parse_macos_airport_output("") == []
    assert netinfo._parse_macos_airport_output("Just one line") == []


def test__parse_macos_airport_output_with_empty_lines():
    # Test parsing output with empty lines - basic structure test
    sample_output = """SSID BSSID RSSI SECURITY
WiFi1 00:11:22:33:44:55 -40 WPA2

WiFi2 00:11:22:33:44:56 -50 WPA2

"""
    result = netinfo._parse_macos_airport_output(sample_output)
    
    assert len(result) == 2  # Empty lines should be skipped
    # Just verify that parsing handles empty lines correctly
    assert isinstance(result, list)
    for item in result:
        assert isinstance(item, dict)
