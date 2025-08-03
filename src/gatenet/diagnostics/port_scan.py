import socket
from typing import List, Tuple
from gatenet.utils import COMMON_PORTS
import asyncio

def check_public_port(host: str = "1.1.1.1", port: int = 53, timeout: float = 2.0) -> bool:
    """
    Check if a TCP port is publicly reachable.

    Example:
        >>> from gatenet.diagnostics.port_scan import check_public_port
        >>> check_public_port("1.1.1.1", 53)
        True
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False
    
def scan_ports(host: str, ports: List[int] = COMMON_PORTS, timeout: float = 2.0) -> List[Tuple[int, bool]]:
    """
    Scan a list of ports on a given host to check if they are open.

    Example:
        >>> from gatenet.diagnostics.port_scan import scan_ports
        >>> scan_ports("localhost", ports=[22, 80, 443])
        [(22, False), (80, True), (443, True)]
    """
    results = []
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((host, port))
                results.append((port, result == 0))
        except Exception:
            results.append((port, False))
    return results

import contextlib

async def check_port(host: str, port: int) -> Tuple[int, bool]:
    """
    Asynchronously check if a TCP port is open on a given host.

    Example:
        >>> import asyncio
        >>> from gatenet.diagnostics.port_scan import check_port
        >>> asyncio.run(check_port("localhost", 22))
        (22, False)
    """
    try:
        async with asyncio.timeout(1.0):
            _reader, writer = await asyncio.open_connection(host, port)
            writer.close()
            await writer.wait_closed()
            return port, True
    except (asyncio.TimeoutError, ConnectionRefusedError):
        return port, False
    
async def scan_ports_async(host: str, ports: List[int] = COMMON_PORTS) -> List[Tuple[int, bool]]:
    """
    Asynchronously scan a list of ports on a given host.

    Example:
        >>> import asyncio
        >>> from gatenet.diagnostics.port_scan import scan_ports_async
        >>> asyncio.run(scan_ports_async("localhost", ports=[22, 80]))
        [(22, False), (80, True)]
    """
    tasks = [check_port(host, port) for port in ports]
    results = await asyncio.gather(*tasks)
    return results