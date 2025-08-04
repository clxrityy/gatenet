"""
gatenet.mesh.lora — LoRaRadio for custom LoRa-based messaging and packet handling.

Example:
    from gatenet.mesh.lora import LoRaRadio
    lora = LoRaRadio()
    lora.send_message('Ping', dest='node3')
    packets = lora.receive_packets()
"""

from typing import List, Dict, Optional
import random
from .radio import MeshRadio

class LoRaRadio(MeshRadio):
    """
    LoRaRadio for custom LoRa-based messaging.

    Example:
        >>> from gatenet.mesh.lora import LoRaRadio
        >>> lora = LoRaRadio()
        >>> lora.send_message('Ping', dest='node3')
        >>> packets = lora.receive_packets()
    """
    def send_message(self, msg: str, dest: str, rf_signal=None, frequency: Optional[float] = None) -> bool:
        """
        Send a message to a destination node using LoRa protocol, optionally with RF info.

        Example:
            >>> lora.send_message('Ping', dest='node3', rf_signal={"freq": 915000000}, frequency=915.0)
        """
        packet = {
            "src": "self",
            "dest": dest,
            "msg": self._encrypt(msg),
            "frequency": frequency or 915.0,
            "timestamp": random.randint(100000, 999999),
            "rf_signal": rf_signal
        }
        self.packets.append(packet)
        self._update_topology(dest)
        return True

    def receive_packets(self) -> List[Dict]:
        """
        Receive and decrypt all LoRa packets sent by this node.

        Example:
            >>> lora = LoRaRadio()
            >>> packets = lora.receive_packets()
        """
        return [self._decrypt_packet(pkt) for pkt in self.packets if "frequency" in pkt]
