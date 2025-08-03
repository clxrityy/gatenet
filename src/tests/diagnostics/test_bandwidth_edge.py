"""
Edge case tests for measure_bandwidth.
"""
import socket
import pytest
from gatenet.diagnostics.bandwidth import measure_bandwidth

def test_measure_bandwidth_invalid_host():
    try:
        result = measure_bandwidth("invalid.host")
        assert isinstance(result, dict)
        assert "error" in result or result.get("download_mbps", 0) == 0
    except Exception as e:
        assert isinstance(e, (socket.gaierror, OSError))

def test_measure_bandwidth_zero_duration():
    try:
        result = measure_bandwidth("google.com", duration=0)
        assert isinstance(result, dict)
        assert result.get("download_mbps", 0) == 0 or "error" in result
    except TimeoutError as e:
        assert isinstance(e, TimeoutError)

def test_measure_bandwidth_negative_payload():
    try:
        result = measure_bandwidth("google.com", payload_size=-1)
        assert isinstance(result, dict)
        assert result.get("download_mbps", 0) == 0 or "error" in result
    except TimeoutError as e:
        assert isinstance(e, TimeoutError)