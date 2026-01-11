"""Port scanning utilities.

This module provides functions for identifying open network ports on
a given target. Implementations are designed to be simple, explicit,
and safe by default.
"""

import socket
from typing import Iterable, List

from gatenet.core.models import Port, ScanResult

# Conservative default port set (expand later)
COMMON_TCP_PORTS: dict[int, str] = {
    22: "ssh",
    80: "http",
    443: "https",
}


def _scan_port(target: str, port: int, timeout: float = 0.5) -> bool:
    """Attempt a TCP connection to a specific port on the target.

    Returns:
        True if the port is open, False otherwise.

    ```py
    is_open = _scan_port("example.com", 22)
    ```
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        try:
            sock.connect((target, port))
            return True
        except (socket.timeout, OSError):
            return False


def scan_target(
    target: str,
    ports: Iterable[int] | None = None,
) -> ScanResult:
    """Scan a target for open TCP ports using a connect scan.

    This function attempts to establish TCP connections against a
    predefined or user-supplied set of ports. It does not perform
    banner grabbing or service fingerprinting.

    Args:
        target: IP address or hostname to scan.
        ports: Optional iterable of TCP ports to scan.

    Returns:
        Structured scan results for the target.

    ```py
    from gatenet.scan.ports import scan_target

    result = scan_target("example.com")

    for port in result.open_ports:
        print(port.number, port.service)
    ```
    """
    open_ports: List[Port] = []

    port_list = ports or COMMON_TCP_PORTS.keys()

    for port in port_list:
        if _scan_port(target, port):
            service = COMMON_TCP_PORTS.get(port)
            open_ports.append(Port(number=port, protocol="tcp", service=service))

    return ScanResult(target=target, open_ports=open_ports)
