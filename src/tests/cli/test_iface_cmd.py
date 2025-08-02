"""
test_iface.py — Tests for the 'iface' CLI command.
"""

import pytest
import argparse
from gatenet.cli.commands.iface import cmd_iface
from unittest.mock import patch


def test_cmd_iface_prints_interfaces(capsys):
    # Patch list_network_interfaces to return a fake list
    with patch("gatenet.utils.list_network_interfaces") as mock_list:
        mock_list.return_value = [
            {"name": "eth0", "ip": "192.168.1.10", "mac": "AA:BB:CC:DD:EE:FF"},
            {"name": "lo", "ip": "127.0.0.1", "mac": ""},
        ]
        cmd_iface(argparse.Namespace())
        out = capsys.readouterr().out
        assert "eth0" in out
        assert "192.168.1.10" in out
        assert "AA:BB:CC:DD:EE:FF" in out
        assert "lo" in out
        assert "127.0.0.1" in out


def test_cmd_iface_no_interfaces(capsys):
    with patch("gatenet.utils.list_network_interfaces", return_value=[]):
        with pytest.raises(SystemExit):
            cmd_iface(argparse.Namespace())
        out = capsys.readouterr().out
        assert "No network interfaces found" in out
