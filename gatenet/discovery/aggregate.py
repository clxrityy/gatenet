import asyncio
from typing import Iterable, List

from gatenet.core.models import Device
from gatenet.discovery.base import AsyncDiscoveryProvider, DiscoveryProvider
from gatenet.discovery.arp import ArpDiscovery
from gatenet.discovery.resolve import resolve_hostnames


DEFAULT_PROVIDERS: list[DiscoveryProvider] = [
    ArpDiscovery(),
    # BluetoothDiscovery(),  # Disabled by default due to dependency
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
    unique: dict[str | int, Device] = {}

    for device in devices:
        if not device.ip:
            # Non-IP devices (e.g. Bluetooth) are not deduped here yet
            unique[id(device)] = device
            continue

        if device.ip not in unique:
            unique[device.ip] = device
            continue

        existing = unique[device.ip]

        if not existing.hostname and device.hostname:
            existing.hostname = device.hostname

        existing.services.extend(device.services)

    return list(unique.values())


async def discover_devices_async(
    *,
    providers: Iterable[DiscoveryProvider],
    resolve_names: bool = False,
) -> List[Device]:
    """Asynchronously discover devices using all configured discovery providers.

    Args:
        providers: An iterable of DiscoveryProvider instances to use.
        resolve_names: Whether to resolve hostnames for discovered devices.

    Returns:
        A list of discovered Device instances.

    ```py
    devices = await discover_devices_async(providers=providers)
    ```
    """
    devices: list[Device] = []

    async_tasks = []

    for provider in providers:
        if isinstance(provider, AsyncDiscoveryProvider):
            async_tasks.append(provider.discover_async())
        else:
            try:
                devices.extend(provider.discover())
            except Exception:
                # Discovery must never be fatal
                continue

    if async_tasks:
        results: list[Iterable[Device] | BaseException] = await asyncio.gather(
            *async_tasks, return_exceptions=True
        )
        for result in results:
            if isinstance(result, BaseException):
                continue
            else:
                devices.extend(result)

    devices = _deduplicate(devices)

    if resolve_names:
        resolve_hostnames(devices)

    return devices


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
