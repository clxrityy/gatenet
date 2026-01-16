from typing import Iterable, List
import platform
import subprocess

from gatenet.core.models import Device
from gatenet.discovery.base import DiscoveryProvider


class ArpDiscovery(DiscoveryProvider):
    """Discover devices on the local network using ARP.

    This provider executes the ARP command to retrieve the list of devices
    currently known to the system.

    ```py
    arp_discovery = ArpDiscovery()
    ```
    """

    name = "arp"

    def discover(self) -> Iterable[Device]:
        """Discover devices using the ARP command.

        Returns:
            An iterable of Device instances discovered via ARP.

        ```py
        devices = arp_discovery.discover()
        ```
        """
        system = platform.system().lower()
        if system == "darwin":
            cmd = ["arp", "-a"]
        elif system == "linux":
            cmd = ["ip", "neigh"]
        else:
            # Windows or unsupported OS
            return []

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError:
            return []

        return _parse_arp_output(result.stdout)


def _parse_arp_output(output: str) -> List[Device]:
    """Parse the output of the ARP command to extract device information.

    Supports common Unix-like ARP formats.

    Returns:
        A list of Device instances discovered via ARP.

    ```py
    devices = _parse_arp_output(arp_command_output)
    ```
    """
    devices: List[Device] = []

    for line in output.splitlines():
        # Skip header or empty lines
        if not line or "?" in line or "Address" in line:
            continue

        parts = line.split()
        ip = parts[0]

        # Very lightweight validation
        if "." not in ip:
            continue

        devices.append(
            Device(
                id=ip,
                kind="ip",
                transport="arp",
                ip=ip,
                hostname=None,
                services=[],
            )
        )

    return devices
