import platform
import subprocess
import asyncio
import re
import time
from typing import Dict, Union
import ipaddress
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
    """Ping a host with optional RF signal logging (stub implementation).
    
    This is a compatibility function that performs a regular ping and adds
    an empty RF field for future radio functionality integration.

    Args:
        host (str): Host to ping
        radio: Radio instance (currently unused - for future implementation)
        count (int): Number of pings
        timeout (int): Timeout per ping
        method (str): Ping method

    Returns:
        dict: Ping results with an empty 'rf' field for compatibility

    Example:
        >>> from gatenet.diagnostics.ping import ping_with_rf
        >>> result = ping_with_rf("8.8.8.8", count=2)
        >>> assert "rf" in result
    """
    result = ping(host, count=count, timeout=timeout, method=method)
    # Add empty RF field for compatibility with radio integration tests
    result["rf"] = []
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


PING_INVALID_HOST_ERROR = "Invalid host format"

def _tcp_ping_sync(host: str, count: int, timeout: int) -> Dict[str, Union[str, float, int, bool, list]]:
    import socket
    if not _is_valid_host(host):
        return {
            "host": host,
            "success": False,
            "error": PING_INVALID_HOST_ERROR,
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
    # Use a hardcoded allowlist for the ping command and never pass unchecked user input
    if not _is_valid_host(host):
        return {
            "host": host,
            "success": False,
            "error": PING_INVALID_HOST_ERROR,
            "raw_output": ""
        }
    # Only allow the system ping command and validated arguments
    # Only allow a validated host (IPv4, IPv6, DNS) and never pass unchecked user input to subprocess
    # This is safe: host is strictly validated, and only appended as a positional argument
    PING_COMMANDS = {
        "Windows": ["ping"],
        "Linux": ["ping"],
        "Darwin": ["ping"]
    }
    cmd = PING_COMMANDS.get(system, ["ping"]).copy()
    if system == "Windows":
        cmd += ["-n", str(count), "-w", str(timeout * 1000)]
    else:
        cmd += ["-c", str(count), "-W", str(timeout)]
    # Host is only appended after passing allowlist validation
    cmd.append(host)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False, shell=False)
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

from gatenet.core import hooks, events


def ping(host: str, count: int = 4, timeout: int = 2, method: str = "icmp") -> Dict[str, Union[str, float, int, bool, list]]:
    """
    Ping a host and return detailed latency statistics, including jitter and all RTTs.

    Example:
        >>> from gatenet.diagnostics.ping import ping
        >>> result = ping("google.com", count=5, method="icmp")
        >>> print(result["rtt_avg"])
    """
    system = platform.system()
    try:
        hooks.emit(events.PING_BEFORE, host=host, count=count)
    except Exception:
        pass
    if method == "icmp":
        result = _icmp_ping_sync(host, count, timeout, system)
    elif method == "tcp":
        result = _tcp_ping_sync(host, count, timeout)
    else:
        result = {
            "host": host,
            "success": False,
            "error": f"Unknown method: {method}",
            "raw_output": ""
        }
    try:
        hooks.emit(events.PING_AFTER, host=host, result=result)
    except Exception:
        pass
    return result

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
        hooks.emit(events.PING_BEFORE, host=host, count=count)
    except Exception:
        pass
    try:
        async with asyncio.timeout(10):
            if method == "icmp":
                result = await _icmp_ping_async(host, count, system)
            elif method == "tcp":
                result = await _tcp_ping_async(host, count)
            else:
                result = {
                    "host": host,
                    "success": False,
                    "error": f"Unknown method: {method}",
                    "raw_output": ""
                }
            try:
                hooks.emit(events.PING_AFTER, host=host, result=result)
            except Exception:
                pass
            return result
    except asyncio.TimeoutError:
        result = {
            "host": host,
            "success": False,
            "error": "Ping operation timed out",
            "raw_output": ""
        }
        try:
            hooks.emit(events.PING_AFTER, host=host, result=result)
        except Exception:
            pass
        return result