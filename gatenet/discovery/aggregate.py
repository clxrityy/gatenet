from typing import Dict, List

from gatenet.core.models import Device
from gatenet.discovery.arp import discover_arp
from gatenet.discovery.resolve import resolve_hostnames


def _deduplicate(devices: List[Device]) -> List[Device]:
    """Deduplice devices by IP address.

    If multiple Device objects share the same IP, their data is merged.
    Hostnames and services are preserved when available.

    Returns:
        A list of unique devices keyed by IP.

    ```py
    devices = [
      Device(ip="192.168.1.1", hostname=None, services=[]),
      Device(ip="192.168.1.1", hostname="router.local", services=[]),
    ]

    unique = _deduplicate(devices)
    assert len(unique) == 1
    assert unique[0].hostname == "router.local"
    ```
    """
    unique: Dict[str, Device] = {}

    for device in devices:
        if device.ip not in unique:
            unique[device.ip] = device
            continue

        existing = unique[device.ip]

        # Prefer non-null hostname
        if not existing.hostname and device.hostname:
            existing.hostname = device.hostname

        # Merge services (naive but safe)
        existing.services.extend(device.services)

    return list(unique.values())


def discover_devices(resolve_names: bool = False) -> List[Device]:
    """Discover devices on the local network.

    Aggregates results from all enabled discovery mechanisms and
    optionally resolves hostnames via reverse DNS.

    Args:
        resolve_names: Whether to perform reverse DNS lookups.

    Returns:
        A deduplicated list of discovered devices.

    ```py
    from gatenet.discovery import discover_devices

    devices = discover_devices(resolve_names=True)
    for device in devices:
        print(device.ip, device.hostname)
    ```
    """
    devices: List[Device] = []

    # v1 discovery sources
    devices.extend(discover_arp())

    devices = _deduplicate(devices)

    if resolve_names:
        resolve_hostnames(devices)

    return devices
