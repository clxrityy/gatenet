"""
Edge case tests for constants.
"""
import pytest
from gatenet.utils.constants import COMMON_PORTS

def test_common_ports_type():
    assert isinstance(COMMON_PORTS, list)
    assert all(isinstance(p, int) for p in COMMON_PORTS)

def test_common_ports_nonempty():
    assert len(COMMON_PORTS) > 0
