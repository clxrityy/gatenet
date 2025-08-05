import platform
import subprocess
import asyncio
import re
import time
from typing import Dict, Union

import ipaddress
from gatenet.radio.sdr import SDRRadio
from gatenet.radio.lora import LoRaRadio
from gatenet.radio.esp import ESPRadio
import re
import statistics
def _is_valid_host(host: str) -> bool:
    """Validate that host is a valid IPv4/IPv6 address or DNS hostname, and does not contain shell-special characters."""
    import socket
    if not host:
        return False
    # Disallow hosts that start with a dash (could be interpreted as an option)
    if host.startswith('-'):
        return False
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-.")
    if any(c not in allowed for c in host):
        return False
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        pass
    if len(host) > 253:
        return False
    hostname_regex = re.compile(
        r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*\.?$"
    )
    if not hostname_regex.match(host):
        return False
    try:
        socket.gethostbyname(host)
        return True
    except Exception:
        return False
def ping_with_rf(host: str, radio=None, count: int = 4, timeout: int = 2, method: str = "icmp") -> Dict[str, Union[str, float, int, bool, list]]:
    """Ping a host and log RF signal info if radio is provided.

    Args:
        host (str): Host to ping
        radio: SDRRadio, LoRaRadio, or ESPRadio instance
        count (int): Number of pings
        timeout (int): Timeout per ping
        method (str): Ping method

    Returns:
        dict: Ping results, optionally with RF info

    Example:
        >>> from gatenet.diagnostics.ping import ping_with_rf
        >>> from gatenet.radio.lora import LoRaRadio
        >>> radio = LoRaRadio()
        >>> result = ping_with_rf("8.8.8.8", radio=radio)
    """
    result = ping(host, count=count, timeout=timeout, method=method)
    if radio:
        rf_results = []
        def handler(info):
            rf_results.append(info)
        radio.on_signal(handler)
        # Use appropriate scan range for each radio type
        if isinstance(radio, SDRRadio):
            radio.scan_frequencies(433_000_000, 434_000_000, 10)
        elif isinstance(radio, LoRaRadio):
            radio.scan_frequencies(868_000_000, 869_000_000, 125)
        elif isinstance(radio, ESPRadio):
            radio.scan_frequencies(2400_000_000, 2483_500_000, 1000)
        result["rf"] = rf_results
    return result

def _parse_ping_output(output: str) -> Dict[str, Union[bool, int, float, str, list]]:
    if "unreachable" in output.lower() or "could not find host" in output.lower():
        return {
            "success": False,
            "error": "Host unreachable or not found"
        }
    stats: Dict[str, Union[bool, int, float, str, list]] = {"success": True}
    # Linux/macOS format
    rtt_match = re.search(r"rtt min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+)", output)
    loss_match = re.search(r"(\d+)% packet loss", output)
    rtt_list = re.findall(r'time=([\d.]+) ms', output)
    rtts = [float(rtt) for rtt in rtt_list]
    if rtts:
        stats["rtts"] = rtts
        stats["jitter"] = statistics.stdev(rtts) if len(rtts) > 1 else 0.0
    # Windows format
    if not rtt_match:
        rtt_match = re.search(r"Minimum = ([\d.]+)ms, Maximum = ([\d.]+)ms, Average = ([\d.]+)ms", output)
        if rtt_match:
            stats["rtt_min"] = float(rtt_match.group(1))
            stats["rtt_max"] = float(rtt_match.group(2))
            stats["rtt_avg"] = float(rtt_match.group(3))
    else:
        stats["rtt_min"] = float(rtt_match.group(1))
        stats["rtt_avg"] = float(rtt_match.group(2))
        stats["rtt_max"] = float(rtt_match.group(3))
        stats["jitter"] = float(rtt_match.group(4))
    if loss_match:
        stats["packet_loss"] = int(loss_match.group(1))
    return stats


def _tcp_ping_sync(host: str, count: int, timeout: int) -> Dict[str, Union[str, float, int, bool, list]]:
    import socket
    if not _is_valid_host(host):
        return {
            "host": host,
            "success": False,
            "error": "Invalid host format",
            "raw_output": ""
        }
    rtts = []
    port = 80
    for _ in range(count):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            start = time.time()
            s.connect((host, port))
            rtt = (time.time() - start) * 1000
            rtts.append(rtt)
            s.close()
        except Exception:
            rtts.append(None)
    valid_rtts = [r for r in rtts if r is not None]
    packet_loss = int(100 * (1 - len(valid_rtts) / count))
    result = {
        "host": host,
        "success": bool(valid_rtts),
        "rtts": valid_rtts,
        "packet_loss": packet_loss,
        "raw_output": "",
    }
    if valid_rtts:
        result["rtt_min"] = min(valid_rtts)
        result["rtt_max"] = max(valid_rtts)
        result["rtt_avg"] = sum(valid_rtts) / len(valid_rtts)
        result["jitter"] = statistics.stdev(valid_rtts) if len(valid_rtts) > 1 else 0.0
    else:
        result["error"] = "All TCP pings failed"
    return result

def _icmp_ping_sync(host: str, count: int, timeout: int, system: str) -> Dict[str, Union[str, float, int, bool, list]]:
    # Harden host validation: only allow valid IPv4, IPv6, or DNS hostnames (no shell metacharacters)
    if not _is_valid_host(host):
        return {
            "host": host,
            "success": False,
            "error": "Invalid host format",
            "raw_output": ""
        }
    # Only allow validated host, never pass unchecked user input to subprocess
    safe_args = ["ping"]
    if system == "Windows":
        safe_args += ["-n", str(count), "-w", str(timeout * 1000)]
    else:
        safe_args += ["-c", str(count), "-W", str(timeout)]
    # Enforce strict allowlist for host before subprocess
    if not _is_valid_host(host):
        return {
            "host": host,
            "success": False,
            "error": "Invalid host format",
            "raw_output": ""
        }
    safe_args.append(host)
    try:
        result = subprocess.run(safe_args, capture_output=True, text=True, check=False, shell=False)
        stats = _parse_ping_output(result.stdout)
        stats.update({
            "host": host,
            "raw_output": result.stdout.strip(),
        })
        return stats
    except Exception as e:
        return {
            "host": host,
            "success": False,
            "error": str(e),
            "raw_output": ""
        }

def ping(host: str, count: int = 4, timeout: int = 2, method: str = "icmp") -> Dict[str, Union[str, float, int, bool, list]]:
    """
    Ping a host and return detailed latency statistics, including jitter and all RTTs.

    Example:
        >>> from gatenet.diagnostics.ping import ping
        >>> result = ping("google.com", count=5, method="icmp")
        >>> print(result["rtt_avg"])
    """
    system = platform.system()
    if method == "icmp":
        return _icmp_ping_sync(host, count, timeout, system)
    elif method == "tcp":
        return _tcp_ping_sync(host, count, timeout)
    else:
        return {
            "host": host,
            "success": False,
            "error": f"Unknown method: {method}",
            "raw_output": ""
        }

async def _tcp_ping_async(host: str, count: int) -> Dict[str, Union[str, float, int, bool, list]]:
    """
    Asynchronously perform TCP ping to a host using a timeout context manager.

    Parameters
    ----------
    host : str
        The hostname or IP address to ping.
    count : int
        Number of echo requests to send.

    Returns
    -------
    dict
        Dictionary with keys: success, rtt_min, rtt_avg, rtt_max, jitter, rtts (list), packet_loss, error, host, raw_output.
    """
    import socket
    import functools
    rtts = []
    port = 80
    loop = asyncio.get_event_loop()
    for _ in range(count):
        try:
            async with asyncio.timeout(2):  # Default timeout of 2 seconds per ping
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                start = time.time()
                await loop.run_in_executor(None, functools.partial(s.connect, (host, port)))
                rtt = (time.time() - start) * 1000
                rtts.append(rtt)
                s.close()
        except Exception:
            rtts.append(None)
    valid_rtts = [r for r in rtts if r is not None]
    packet_loss = int(100 * (1 - len(valid_rtts) / count))
    result = {
        "host": host,
        "success": bool(valid_rtts),
        "rtts": valid_rtts,
        "packet_loss": packet_loss,
        "raw_output": "",
    }
    if valid_rtts:
        result["rtt_min"] = min(valid_rtts)
        result["rtt_max"] = max(valid_rtts)
        result["rtt_avg"] = sum(valid_rtts) / len(valid_rtts)
        result["jitter"] = statistics.stdev(valid_rtts) if len(valid_rtts) > 1 else 0.0
    else:
        result["error"] = "All TCP pings failed"
    return result

async def _icmp_ping_async(host: str, count: int, system: str) -> Dict[str, Union[str, float, int, bool, list]]:
    if system == "Windows":
        cmd = ["ping", "-n", str(count), host]
    else:
        cmd = ["ping", "-c", str(count), host]
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _stderr = await process.communicate()
        output = stdout.decode()
        stats = _parse_ping_output(output)
        stats.update({
            "host": host,
            "raw_output": output.strip(),
        })
        return stats
    except Exception as e:
        return {
            "host": host,
            "success": False,
            "error": str(e),
            "raw_output": ""
        }

async def async_ping(
    host: str,
    count: int = 4,
    method: str = "icmp"
) -> Dict[str, Union[str, float, int, bool, list]]:
    """
    Asynchronously ping a host and return detailed latency statistics, including jitter and all RTTs.

    Example:
        >>> from gatenet.diagnostics.ping import async_ping
        >>> import asyncio
        >>> result = asyncio.run(async_ping("google.com", count=5, method="icmp"))
        >>> print(result["rtt_avg"])
    """
    system = platform.system()
    try:
        async with asyncio.timeout(10):
            if method == "icmp":
                return await _icmp_ping_async(host, count, system)
            elif method == "tcp":
                return await _tcp_ping_async(host, count)
            else:
                return {
                    "host": host,
                    "success": False,
                    "error": f"Unknown method: {method}",
                    "raw_output": ""
                }
    except asyncio.TimeoutError:
        return {
            "host": host,
            "success": False,
            "error": "Ping operation timed out",
            "raw_output": ""
        }