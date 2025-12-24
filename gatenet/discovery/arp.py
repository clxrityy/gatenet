from typing import List

from gatenet.core.models import Device


def discover_arp() -> List[Device]:
    """
    Discover devices using ARP scanning.

    This is a placeholder implementation that will be
    replaced with a real ARP scan in a later iteration.

    Returns:
        list[Device]: Devices discovered via ARP.
    """
    return [
        Device(ip="192.168.1.1", hostname="router.local", services=[]),
        Device(ip="192.168.1.42", hostname="laptop.local", services=[]),
    ]