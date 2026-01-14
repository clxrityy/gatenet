from typing import Iterable, List

from gatenet.core.models import Device
from gatenet.discovery.base import DiscoveryProvider
from gatenet.discovery.arp import ArpDiscovery
from gatenet.discovery.resolve import resolve_hostnames


DEFAULT_PROVIDERS: list[DiscoveryProvider] = [
    ArpDiscovery(),
]


def _deduplicate(devices: Iterable[Device]) -> list[Device]:
    """Deduplicate devices based on their IP addresses.

    If multiple devices share the same IP, their information is merged.
    Hostnames and services are preserved where possible.

    Args:
        devices: An iterable of Device instances to deduplicate.

    Returns:
        A list of unique Device instances.

    ```py
    unique_devices = _deduplicate(devices)
    ```
    """
    unique: dict[str, Device] = {}

    for device in devices:
        if not device.ip:
            # Non-IP devices (e.g. Bluetooth) are not deduped here yet
            unique[str(id(device))] = device
            continue

        if device.ip not in unique:
            unique[device.ip] = device
            continue

        existing = unique[device.ip]

        if not existing.hostname and device.hostname:
            existing.hostname = device.hostname

        existing.services.extend(device.services)

    return list(unique.values())


def discover_devices(
    *,
    resolve_names: bool = False,
    providers: Iterable[DiscoveryProvider] | None = None,
) -> List[Device]:
    """Discover devices using all configured discovery providers.

    Args:
        resolve_names: Whether to resolve hostnames for discovered devices.
        providers: An optional iterable of DiscoveryProvider instances to use.

    Returns:
        A list of discovered Device instances.

    ```py
    devices = discover_devices()
    ```
    """
    devices: list[Device] = []

    for provider in providers or DEFAULT_PROVIDERS:
        try:
            devices.extend(provider.discover())
        except Exception:
            # Discovery must never be fatal
            continue

    devices = _deduplicate(devices)

    if resolve_names:
        resolve_hostnames(devices)

    return devices
