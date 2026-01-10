import platform
import subprocess
from typing import List

from gatenet.core.models import Device


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

        devices.append(Device(ip=ip, hostname=None, services=[]))

    return devices


def discover_arp() -> List[Device]:
    """Discover devices using ARP-based techniques.

    This reads the local ARP table and converts known entries into
    Device objects. This method is passive and does not emit packets.

    Returns:
        Devices discovered via ARP.

    ```py
    devices = discover_arp()
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
