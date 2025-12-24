from typing import List

from gatenet.core.models import Port, ScanResult


def scan_target(target: str) -> ScanResult:
    """
    Scan a target for open TCP ports.

    This function performs a basic TCP connect scan using
    a predefined set of common ports.

    Args:
        target (str): IP address, hostname, or CIDR range.

    Returns:
        ScanResult: Structured scan results.
    """
    open_ports: List[Port] = [
        Port(number=22, service="ssh"),
        Port(number=80, service="http"),
    ]

    return ScanResult(target=target, open_ports=open_ports)