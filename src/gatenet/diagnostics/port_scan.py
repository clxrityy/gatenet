import socket
from typing import List, Tuple
from gatenet.utils import COMMON_PORTS
import asyncio

def check_public_port(host: str = "1.1.1.1", port: int = 53, timeout: float = 2.0) -> bool:
    """
    Check if a TCP port is publicly reachable.

    :param host: The public IP or domain name to test.
    :param port: The port number to test.
    :param timeout: Timeout in seconds for the connection attempt.
    :return: True if the port is reachable, False otherwise.
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False
    
def scan_ports(host: str, ports: List[int] = COMMON_PORTS, timeout: float = 2.0) -> List[Tuple[int, bool]]:
    """
    Scan a list of ports on a given host to check if they are open.
    
    :param host: The host to scan (IP address or domain name).
    :param ports: A list of port numbers to scan. Defaults to COMMON_PORTS.
    :param timeout: Timeout in seconds for each port check.
    :return: A list of tuples where each tuple contains the port number and a boolean indicating if it is open.
    """
    open_ports = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            if result == 0:
                open_ports.append((port, True))
            else:
                open_ports.append((port, False))
    return open_ports

async def check_port(host: str, port: int, timeout: float = 1.0) -> Tuple[int, bool]:
    try:
        _reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout)
        writer.close()
        await writer.wait_closed()
        return port, True
    except (asyncio.TimeoutError, ConnectionRefusedError):
        return port, False
    
async def scan_ports_async(host: str, ports: List[int] = COMMON_PORTS, timeout: float = 1.0) -> List[Tuple[int, bool]]:
    tasks = [check_port(host, port, timeout) for port in ports]
    results = await asyncio.gather(*tasks)
    return results