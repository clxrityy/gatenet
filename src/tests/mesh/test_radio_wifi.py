"""
Tests for MeshRadio Wi-Fi scanning and correlation (mock and real scan).
Run with: pytest src/tests/mesh/test_radio_wifi.py
"""
import pytest
from gatenet.mesh import MeshRadio

def test_wifi_scan_mock():
    mesh = MeshRadio()
    networks = mesh.scan_wifi(mock=True)
    assert isinstance(networks, list)
    assert any(n["ssid"] == "TestNet" for n in networks)
    assert any(n["ssid"] == "HomeWiFi" for n in networks)
    assert mesh.topology["wifi"] == networks

def test_wifi_scan_empty():
    mesh = MeshRadio()
    mesh.wifi_networks = []
    mesh.topology["wifi"] = []
    assert mesh.scan_wifi(mock=True) != []

def test_wifi_scan_real(monkeypatch):
    mesh = MeshRadio()
    # Patch subprocess.check_output to simulate iwlist output
    def fake_check_output(cmd, text):
        return '''Cell 01 - Address: AA:BB:CC:DD:EE:FF\nESSID:"TestNet"\nSignal level=-40\nCell 02 - Address: 11:22:33:44:55:66\nESSID:"HomeWiFi"\nSignal level=-60'''
    monkeypatch.setattr("subprocess.check_output", fake_check_output)
    networks = mesh.scan_wifi(interface="wlan0", mock=False)
    assert any(n["ssid"] == "TestNet" for n in networks)
    assert any(n["mac"] == "AA:BB:CC:DD:EE:FF" for n in networks)
    assert any(n["signal"] == -40 for n in networks)
    assert mesh.topology["wifi"] == networks

def test_wifi_scan_error(monkeypatch):
    mesh = MeshRadio()
    def fake_check_output(cmd, text):
        raise OSError("iwlist not found")
    monkeypatch.setattr("subprocess.check_output", fake_check_output)
    networks = mesh.scan_wifi(interface="wlan0", mock=False)
    assert networks[0]["error"] == "iwlist not found"
    assert mesh.topology["wifi"] == networks
