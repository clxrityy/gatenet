import socket
from typing import List, Tuple
from gatenet.utils import COMMON_PORTS
import asyncio

def check_public_port(host: str = "1.1.1.1", port: int = 53, timeout: float = 2.0) -> bool:
    """
    Check if a TCP port is publicly reachable.

    Args:
        host (str): The public IP or domain name to test.
        port (int): The port number to test.
        timeout (float): Timeout in seconds for the connection attempt.

    Returns:
        bool: True if the port is reachable, False otherwise.
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False
    
def scan_ports(host: str, ports: List[int] = COMMON_PORTS, timeout: float = 2.0) -> List[Tuple[int, bool]]:
    """
    Scan a list of ports on a given host to check if they are open.

    Args:
        host (str): The host to scan (IP address or domain name).
        ports (List[int]): A list of port numbers to scan. Defaults to COMMON_PORTS.
        timeout (float): Timeout in seconds for each port check.

    Returns:
        List[Tuple[int, bool]]: A list of tuples (port, is_open).
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

    Args:
        host (str): The host to check.
        port (int): The port number to check.

    Returns:
        Tuple[int, bool]: (port, is_open)
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

    Args:
        host (str): The host to scan.
        ports (List[int]): List of port numbers to scan. Defaults to COMMON_PORTS.

    Returns:
        List[Tuple[int, bool]]: List of (port, is_open) tuples.
    """
    tasks = [check_port(host, port) for port in ports]
    results = await asyncio.gather(*tasks)
    return results