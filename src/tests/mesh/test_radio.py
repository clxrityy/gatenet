"""
Tests for gatenet.mesh radio classes: MeshRadio, LoRaRadio, ESPRadio.

Covers:
- Packet sending/receiving
- Encryption/decryption
- Topology tracking
- Protocol-specific features (frequency/channel)

Run with: pytest src/tests/mesh/test_radio.py
"""
import pytest
from gatenet.mesh import MeshRadio, LoRaRadio, ESPRadio

def test_meshradio_send_and_receive():
    mesh = MeshRadio()
    assert mesh.send_message("Hello", dest="node2")
    packets = mesh.receive_packets()
    assert isinstance(packets, list)
    assert packets[0]["msg"] == "Hello"
    assert packets[0]["dest"] == "node2"
    topo = mesh.get_topology()
    assert "node2" in topo["nodes"]
    assert {"src": "self", "dest": "node2"} in topo["links"]

def test_meshradio_encryption():
    mesh = MeshRadio()
    mesh.send_message("Secret", dest="nodeX")
    raw = mesh.packets[0]["msg"]
    assert raw.startswith("enc(")
    packets = mesh.receive_packets()
    assert packets[0]["msg"] == "Secret"

def test_loraradio_frequency():
    lora = LoRaRadio()
    lora.send_message("Ping", dest="lora1", frequency=433.0)
    packets = lora.receive_packets()
    assert packets[0]["frequency"] == pytest.approx(433.0)
    assert packets[0]["msg"] == "Ping"
    topo = lora.get_topology()
    assert "lora1" in topo["nodes"]

def test_loraradio_default_frequency():
    lora = LoRaRadio()
    lora.send_message("Ping", dest="lora2")
    packets = lora.receive_packets()
    assert packets[0]["frequency"] == pytest.approx(915.0)

def test_espradio_channel():
    esp = ESPRadio()
    esp.send_message("ESPMsg", dest="esp1", channel=6)
    packets = esp.receive_packets()
    assert packets[0]["channel"] == 6
    assert packets[0]["msg"] == "ESPMsg"
    topo = esp.get_topology()
    assert "esp1" in topo["nodes"]

def test_espradio_default_channel():
    esp = ESPRadio()
    esp.send_message("ESPMsg", dest="esp2")
    packets = esp.receive_packets()
    assert packets[0]["channel"] == 1

def test_topology_multiple_nodes():
    mesh = MeshRadio()
    mesh.send_message("A", dest="n1")
    mesh.send_message("B", dest="n2")
    topo = mesh.get_topology()
    assert set(topo["nodes"]) == {"n1", "n2"}
    assert len(topo["links"]) == 2

def test_empty_receive():
    mesh = MeshRadio()
    packets = mesh.receive_packets()
    assert packets == []
