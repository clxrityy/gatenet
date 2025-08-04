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
        from urllib.parse import urlparse
        # Parse output for URLs and validate host
        import re
        urls = re.findall(r'(https?://[\w\.-]+)', out)
        for url in urls:
            host = urlparse(url).hostname
            assert host in ["google.com", "dns.google"]
        assert "8.8.8.8" in out
        # Also check that the output contains the expected hostnames as standalone values
        assert any(h in out for h in ["google.com", "dns.google"])

def test_cmd_dns_error(capsys):
    with patch("gatenet.diagnostics.dns.dns_lookup", return_value="Unknown"), \
         patch("gatenet.diagnostics.dns.reverse_dns_lookup", return_value="Unknown"):
        class Args:
            query = "badhost"
            output = "plain"
        cmd_dns(Args())
        out = capsys.readouterr().out
        assert "error" in out
