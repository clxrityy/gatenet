"""
Integration tests for radio/diagnostics: MeshRadio with ping_with_rf, GPS, RF, Wi-Fi, and messaging.
"""
import pytest
from gatenet.mesh.radio import MeshRadio
from gatenet.diagnostics.ping import ping_with_rf

def test_radio_ping_with_rf_integration():
    radio = MeshRadio()
    # Log GPS and RF before ping
    radio.log_gps(37.7749, -122.4194)
    radio.log_rf_signal({"freq": 868000000, "power": 24, "type": "lora"})
    radio.scan_wifi(mock=True)
    # Use ping_with_rf with MeshRadio (should not fail, but rf will be empty)
    result = ping_with_rf("127.0.0.1", radio=radio, count=1)
    assert "rf" in result
    # MeshRadio does not implement on_signal, so rf should be empty
    assert isinstance(result["rf"], list)
    # Send a message with RF info
    sent = radio.send_message("test", "node2", rf_signal={"freq": 868000000})
    assert sent is True
    packets = radio.receive_packets()
    assert isinstance(packets, list)
    assert packets[0]["msg"] == "test"
    # Topology should include GPS, RF, and Wi-Fi
    topo = radio.get_topology()
    assert "locations" in topo
    assert "signals" in topo
    assert "wifi" in topo
    assert len(topo["locations"]) > 0
    assert len(topo["signals"]) > 0
    assert len(topo["wifi"]) > 0
