"""
Test collision detection for SDRRadio.
"""
import pytest
from gatenet.radio.sdr import SDRRadio

def test_sdrradio_collision_detection():
    radio = SDRRadio()
    collisions = radio.detect_collisions()
    assert isinstance(collisions, list)
    for c in collisions:
        assert "source" in c and "strength" in c
