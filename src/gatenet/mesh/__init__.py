"""
gatenet.mesh — LoRa/Mesh radio interface for encrypted messaging and topology mapping.

Features:
- Parse incoming mesh packets
- Send encrypted messages
- Track and map mesh topology

Example usage:
    from gatenet.mesh import MeshRadio
    mesh = MeshRadio()
    mesh.send_message('Hello', dest='node2')
    packets = mesh.receive_packets()
"""

from .radio import MeshRadio
from .esp import ESPRadio
from .lora import LoRaRadio

__all__ = ["MeshRadio", "ESPRadio", "LoRaRadio"]