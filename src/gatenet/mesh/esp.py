"""
gatenet.mesh.esp — ESPRadio for custom ESP-based messaging and packet handling.

Example:
    from gatenet.mesh.esp import ESPRadio
    esp = ESPRadio()
    esp.send_message('Status', dest='node5')
    packets = esp.receive_packets()
"""

from typing import List, Dict, Optional
from .radio import MeshRadio

import random
from typing import List, Dict, Optional
from .radio import MeshRadio

class ESPRadio(MeshRadio):
    """
    ESPRadio for custom ESP-based messaging.

    Example:
        >>> from gatenet.mesh.esp import ESPRadio
        >>> esp = ESPRadio()
        >>> esp.send_message('Status', dest='node5')
        >>> packets = esp.receive_packets()
    """
    def send_message(self, msg: str, dest: str, rf_signal=None, channel: Optional[int] = None) -> bool:
        """
        Send a message to a destination node using ESP protocol, optionally with RF info.

        Example:
            >>> esp.send_message('Status', dest='node5', rf_signal={"freq": 2400000000}, channel=6)
        """
        packet = {
            "src": "self",
            "dest": dest,
            "msg": self._encrypt(msg),
            "channel": channel or 1,
            "timestamp": random.randint(100000, 999999),
            "rf_signal": rf_signal
        }
        self.packets.append(packet)
        self._update_topology(dest)
        return True

    def receive_packets(self) -> List[Dict]:
        """
        Receive and decrypt all ESP packets sent by this node.

        Example:
            >>> esp = ESPRadio()
            >>> packets = esp.receive_packets()
        """
        return [self._decrypt_packet(pkt) for pkt in self.packets if "channel" in pkt]
