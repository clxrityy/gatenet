import socket
from typing import Iterable

from gatenet.core.models import Device


def resolve_hostnames(devices: Iterable[Device]) -> None:
    """Resolve hostnames for devices using reverse DNS.

    This function mutates Device objects in place.
    Devices that already have hostnames are skipped.

    Resolution failures are silently ignored.

    ```py
    devices = [
      Device(ip="8.8.8.8"),
      Device(ip="192.168.1.1"),
    ]

    resolve_hostnames(devices)

    for device in devices:
      print(f"{device.ip} -> {device.hostname}")
    ```
    """
    for device in devices:
        if device.hostname:
            continue  # Skip already resolved hostnames

        try:
            hostname, _, _ = socket.gethostbyaddr(device.ip)
            device.hostname = hostname
        except (socket.herror, socket.gaierror, TimeoutError):
            # Resolution failed; leave hostname as None
            continue
