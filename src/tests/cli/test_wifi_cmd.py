"""
test_wifi.py — Tests for the 'wifi' CLI command.
"""
import pytest
from gatenet.cli.commands.wifi import cmd_wifi
from unittest.mock import patch


def test_cmd_wifi_prints_networks(capsys):
    with patch("gatenet.utils.scan_wifi_networks") as mock_scan:
        mock_scan.return_value = [
            {"ssid": "TestNet", "signal": "-40", "security": "WPA2"},
            {"ssid": "OpenNet", "signal": "-70", "security": "Open"},
        ]
        cmd_wifi(None)
        out = capsys.readouterr().out
        assert "TestNet" in out
        assert "WPA2" in out
        assert "OpenNet" in out
        assert "Open" in out


def test_cmd_wifi_no_networks(capsys):
    with patch("gatenet.utils.scan_wifi_networks", return_value=[]):
        class Args:
            output = "plain"
        with pytest.raises(SystemExit):
            cmd_wifi(Args())
        out = capsys.readouterr().out
        assert "No Wi-Fi networks found" in out


def test_cmd_wifi_error(capsys):
    with patch("gatenet.utils.scan_wifi_networks", return_value=[{"error": "not supported"}]):
        class Args:
            output = "plain"
        with pytest.raises(SystemExit):
            cmd_wifi(Args())
        out = capsys.readouterr().out
        assert "Error" in out
