"""
Edge case tests for traceroute.
"""
import pytest
from gatenet.diagnostics.traceroute import traceroute

def test_traceroute_invalid_host():
    try:
        hops = traceroute("notarealdomain.tld")
        assert isinstance(hops, list)
        assert len(hops) == 0 or all(isinstance(h, dict) for h in hops)
    except ValueError as e:
        assert "Unable to resolve host" in str(e)

def test_traceroute_zero_max_hops():
    hops = traceroute("google.com", max_hops=0)
    assert isinstance(hops, list)
    assert hops == []