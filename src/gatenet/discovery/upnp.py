import socket
import time
from typing import List, Dict
import re

SSDP_MULTICAST_ADDRESS = "239.255.255.250"
SSDP_PORT = 1900
SSDP_MX = 2
SSDP_ST = "ssdp:all"

def discover_upnp_devices(timeout: float = 3.0) -> List[Dict[str, str]]:
    """
    Discover UPnP devices using SSDP.

    Parameters
    ----------
    timeout : float, optional
        Time in seconds to wait for responses (default is 3.0).

    Returns
    -------
    List[Dict[str, str]]
        List of discovered device info dictionaries.
    """
    message = "\r\n".join([
        'M-SEARCH * HTTP/1.1',
        f'HOST: {SSDP_MULTICAST_ADDRESS}:{SSDP_PORT}',
        'MAN: "ssdp:discover"',
        f'MX: {SSDP_MX}',
        f'ST: {SSDP_ST}',
        '', ''
    ])

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(timeout)
    sock.sendto(message.encode(), (SSDP_MULTICAST_ADDRESS, SSDP_PORT))

    devices = []
    start = time.time()

    while True:
        try:
            if time.time() - start > timeout:
                break
            data, _ = sock.recvfrom(1024)
            response = data.decode(errors="ignore")
            devices.append(_parse_ssdp_response(response))
        except socket.timeout:
            break
        except Exception:
            continue
    sock.close()
    return devices


def _parse_ssdp_response(response: str) -> Dict[str, str]:
    """
    Parse an SSDP response into a dictionary of headers.

    Parameters
    ----------
    response : str
        The SSDP response string.

    Returns
    -------
    Dict[str, str]
        Dictionary of SSDP response headers.
    """
    headers = {}
    lines = response.split("\r\n")
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            headers[key.strip().upper()] = value.strip()
    return headers
