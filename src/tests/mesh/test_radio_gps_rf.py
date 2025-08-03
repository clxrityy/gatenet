"""
Tests for MeshRadio GPS and RF signal logging, packet tagging, and topology tracking.

Run with: pytest src/tests/mesh/test_radio_gps_rf.py
"""
import pytest
from gatenet.mesh import MeshRadio

def test_gps_logging():
    mesh = MeshRadio()
    mesh.log_gps(51.5074, -0.1278)
    assert mesh.gps_location == (51.5074, -0.1278)
    assert mesh.topology["locations"][-1]["lat"] == pytest.approx(51.5074)
    assert mesh.topology["locations"][-1]["lon"] == pytest.approx(-0.1278)

def test_rf_signal_logging():
    mesh = MeshRadio()
    mesh.log_rf_signal(-70.5)
    assert mesh.rf_signal == -70.5
    assert mesh.topology["signals"][-1]["signal"] == -70.5

def test_packet_tags_gps_rf():
    mesh = MeshRadio()
    mesh.log_gps(40.7128, -74.0060)
    mesh.log_rf_signal(-60.0)
    mesh.send_message("Test", dest="nodeX")
    pkt = mesh.packets[-1]
    assert pkt["gps"] == (40.7128, -74.0060)
    assert pkt["rf_signal"] == -60.0
    packets = mesh.receive_packets()
    assert packets[-1]["msg"] == "Test"

def test_topology_multiple_locations_signals():
    mesh = MeshRadio()
    mesh.log_gps(1, 2)
    mesh.log_gps(3, 4)
    mesh.log_rf_signal(-50)
    mesh.log_rf_signal(-55)
    locs = mesh.topology["locations"]
    sigs = mesh.topology["signals"]
    assert locs == [
        {"node": "self", "lat": 1, "lon": 2},
        {"node": "self", "lat": 3, "lon": 4}
    ]
    assert sigs == [
        {"node": "self", "signal": -50},
        {"node": "self", "signal": -55}
    ]

def test_send_message_without_gps_rf():
    mesh = MeshRadio()
    mesh.send_message("NoLoc", dest="nodeY")
    pkt = mesh.packets[-1]
    assert pkt["gps"] is None
    assert pkt["rf_signal"] is None
