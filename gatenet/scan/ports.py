# gatenet/scan/ports.py

from typing import List

from gatenet.core.models import Port, ScanResult


def scan_target(target: str) -> ScanResult:
    """
    Scan a target for open ports.

    Stub implementation for CLI validation.
    """

    open_ports: List[Port] = [
        Port(number=22, service="ssh"),
        Port(number=80, service="http")
    ]

    return ScanResult(
        target=target,
        open_ports=open_ports
    )
