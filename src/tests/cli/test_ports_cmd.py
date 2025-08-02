"""
test_ports.py — Tests for the 'ports' CLI command.
"""
import pytest
from gatenet.cli.commands.ports import cmd_ports
from unittest.mock import patch

def test_cmd_ports_success(capsys):
    with patch("gatenet.diagnostics.port_scan.scan_ports") as mock_scan:
        mock_scan.return_value = [(22, True), (80, False)]
        class Args:
            host = "localhost"
            ports = [22, 80]
            output = "plain"
        cmd_ports(Args())
        out = capsys.readouterr().out
        assert "22" in out
        assert "OPEN" in out or "open" in out
        assert "80" in out
        assert "closed" in out

def test_cmd_ports_error(capsys):
    with patch("gatenet.diagnostics.port_scan.scan_ports", side_effect=Exception("fail")):
        class Args:
            host = "localhost"
            ports = [22, 80]
            output = "plain"
        with pytest.raises(SystemExit):
            cmd_ports(Args())
        out = capsys.readouterr().out
        assert "Error" in out
