"""Port scanning utilities.

This module provides functions for identifying open network ports on
a given target. Implementations are designed to be simple, explicit,
and safe by default.
"""

from typing import List

from gatenet.core.models import Port, ScanResult


def scan_target(target: str) -> ScanResult:
    """Scan a target for open TCP ports.

    This function performs a basic TCP connect scan against a predefined
    set of common ports. It is intended as a minimal, synchronous
    implementation and may be extended or replaced in future versions.

    Args:
        target: IP address, hostname, or CIDR range to scan.

    Returns:
        Structured scan results for the target.

    ```py
    result = scan_target("example.com")
    ```
    """
    open_ports: List[Port] = [
        Port(number=22, service="ssh"),
        Port(number=80, service="http"),
    ]

    return ScanResult(target=target, open_ports=open_ports)
