"""
test_ping.py — Tests for the 'ping' CLI command.
"""
import pytest
from gatenet.cli.commands.ping import cmd_ping
from unittest.mock import patch

def test_cmd_ping_success(capsys):
    with patch("gatenet.diagnostics.ping.ping") as mock_ping:
        mock_ping.return_value = {
            "success": True,
            "rtt_min": 10.0,
            "rtt_avg": 12.5,
            "rtt_max": 15.0,
            "jitter": 1.2,
            "packet_loss": 0
        }
        class Args:
            host = "example.com"
            output = "plain"
        cmd_ping(Args())
        out = capsys.readouterr().out
        assert "min=10.00" in out
        assert "avg=12.50" in out
        assert "max=15.00" in out
        assert "loss=0%" in out

def test_cmd_ping_error(capsys):
    with patch("gatenet.diagnostics.ping.ping", return_value={"success": False, "error": "timeout"}):
        class Args:
            host = "example.com"
            output = "plain"
        with pytest.raises(SystemExit):
            cmd_ping(Args())
        out = capsys.readouterr().out
        assert "Error" in out
