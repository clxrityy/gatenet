"""
test_trace.py — Tests for the 'trace' CLI command.
"""
import pytest
from gatenet.cli.commands.trace import cmd_trace
from unittest.mock import patch


def test_cmd_trace_prints_hops(capsys):
    with patch("gatenet.diagnostics.traceroute.traceroute") as mock_trace:
        mock_trace.return_value = [
            {"hop": 1, "ip": "192.168.1.1", "hostname": "router", "rtt_ms": 2.3},
            {"hop": 2, "ip": "8.8.8.8", "hostname": "dns", "rtt_ms": 10.1},
        ]
        class Args:
            host = "example.com"
            output = "plain"
        cmd_trace(Args())
        out = capsys.readouterr().out
        assert "192.168.1.1" in out
        assert "8.8.8.8" in out
        assert "router" in out
        assert "dns" in out


def test_cmd_trace_no_hops(capsys):
    with patch("gatenet.diagnostics.traceroute.traceroute", return_value=[]):
        class Args:
            host = "example.com"
            output = "plain"
        with pytest.raises(SystemExit):
            cmd_trace(Args())
        out = capsys.readouterr().out
        assert "No hops found" in out or "failed" in out
