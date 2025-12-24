from typing import List

from gatenet.core.models import Device
from gatenet.discovery.arp import discover_arp


def discover_devices() -> List[Device]:
    """
    Discover devices on the local network.

    This function aggregates results from all available
    discovery mechanisms (ARP, mDNS, SSDP, etc.).

    Returns:
        list[Device]: Combined list of discovered devices.
    """
    devices: List[Device] = []

    # NOTE: For v1, only ARP is enabled.
    devices.extend(discover_arp())

    return devices