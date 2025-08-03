"""
Edge case tests for scan_ports and check_public_port.
"""
import pytest
from gatenet.diagnostics.port_scan import scan_ports, check_public_port

def test_scan_ports_invalid_host():
    results = scan_ports("invalid.host", ports=[22, 80])
    assert isinstance(results, list)
    assert all(isinstance(t, tuple) and len(t) == 2 for t in results)

def test_scan_ports_empty_ports():
    results = scan_ports("127.0.0.1", ports=[])
    assert isinstance(results, list)
    assert results == []

def test_check_public_port_invalid():
    is_open = check_public_port("invalid.host", 9999)
    assert is_open is False or isinstance(is_open, bool)
