from typing import List

from gatenet.core.models import Device


def discover_arp() -> List[Device]:
    """
    Discover devices using ARP-based techniques.

    This function is currently a placeholder implementation and returns
    static example data. It will be replaced with a real ARP discovery
    mechanism in a future iteration.

    Returns:
        Devices discovered via ARP.
    """
    return [
        Device(ip="192.168.1.1", hostname="router.local", services=[]),
        Device(ip="192.168.1.42", hostname="laptop.local", services=[]),
    ]
