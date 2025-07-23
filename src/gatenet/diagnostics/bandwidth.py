"""
bandwidth.py

Bandwidth measurement utilities for gatenet.

This module provides functions to measure upload and download bandwidth to a target host using TCP sockets.

Example:
    from gatenet.diagnostics.bandwidth import measure_bandwidth
    result = measure_bandwidth("example.com", port=5201)
    print(result)
"""

import socket
import time
from typing import Dict, Optional

def measure_bandwidth(host: str, port: int = 5201, duration: float = 5.0, payload_size: int = 65536, direction: str = "download") -> Dict[str, float]:
    """
    Example
    -------
    >>> from gatenet.diagnostics.bandwidth import measure_bandwidth
    >>> result = measure_bandwidth("example.com", port=5201, duration=2.0)
    >>> print(result)
    {'bandwidth_mbps': 94.2, 'bytes_transferred': 2359296, 'duration': 2.0}
    Measure bandwidth to a target host using TCP sockets.

    Parameters
    ----------
    host : str
        Target host to connect to.
    port : int, optional
        Target port (default: 5201).
    duration : float, optional
        Duration of the test in seconds (default: 5.0).
    payload_size : int, optional
        Size of each payload in bytes (default: 65536).
    direction : {"download", "upload"}, optional
        Direction of measurement (default: "download").

    Returns
    -------
    dict
        Dictionary with keys 'bandwidth_mbps', 'bytes_transferred', and 'duration'.

    Notes
    -----
    This function requires a bandwidth server (e.g., iperf3) running on the target host.
    """
    assert direction in ("download", "upload"), "direction must be 'download' or 'upload'"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((host, port))
    total_bytes = 0
    start = time.time()
    try:
        if direction == "download":
            while time.time() - start < duration:
                data = s.recv(payload_size)
                if not data:
                    break
                total_bytes += len(data)
        else:
            payload = b"0" * payload_size
            while time.time() - start < duration:
                sent = s.send(payload)
                total_bytes += sent
    finally:
        s.close()
    elapsed = time.time() - start
    bandwidth_mbps = (total_bytes * 8) / (elapsed * 1_000_000)
    return {
        "bandwidth_mbps": bandwidth_mbps,
        "bytes_transferred": total_bytes,
        "duration": elapsed
    }
