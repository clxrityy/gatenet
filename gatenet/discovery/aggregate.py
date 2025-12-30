from typing import List

from gatenet.core.models import Device
from gatenet.discovery.arp import discover_arp


def discover_devices() -> List[Device]:
    """Discover devices on the local network using available methods.

    This function aggregates results from all enabled discovery
    mechanisms (e.g. ARP, mDNS, SSDP) into a single device list.

    The discovery process is observational only and does not modify
    network state.

    Returns:
        A combined list of discovered devices.
    """
    devices: List[Device] = []

    # NOTE: For v1, only ARP discovery is enabled.
    devices.extend(discover_arp())

    return devices
