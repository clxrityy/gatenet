"""
test_dns.py — Tests for the 'dns' CLI command.
"""
import pytest
from gatenet.cli.commands.dns import cmd_dns
from unittest.mock import patch

def test_cmd_dns_success(capsys):
    with patch("gatenet.diagnostics.dns.dns_lookup", return_value="8.8.8.8"), \
         patch("gatenet.diagnostics.dns.reverse_dns_lookup", return_value="dns.google"):
        class Args:
            query = "google.com"
            output = "plain"
        cmd_dns(Args())
        out = capsys.readouterr().out
        assert "google.com" in out
        assert "8.8.8.8" in out
        assert "dns.google" in out

def test_cmd_dns_error(capsys):
    with patch("gatenet.diagnostics.dns.dns_lookup", return_value="Unknown"), \
         patch("gatenet.diagnostics.dns.reverse_dns_lookup", return_value="Unknown"):
        class Args:
            query = "badhost"
            output = "plain"
        cmd_dns(Args())
        out = capsys.readouterr().out
        assert "error" in out
