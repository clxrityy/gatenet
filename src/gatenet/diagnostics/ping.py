import platform
import subprocess
import asyncio
import re
from typing import Dict, Union

def _parse_ping_output(output: str) -> Dict[str, Union[bool, int, float, str]]:
    if "unreachable" in output.lower() or "could not find host" in output.lower():
        return {
            "success": False,
            "error": "Host unreachable or not found"
        }
    
    # Fix: Explicitly type the stats dictionary to accept multiple types
    stats: Dict[str, Union[bool, int, float, str]] = {
        "success": True
    }
    
    # Linux/macOS format
    rtt_match = re.search(r"rtt min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/([\d.]+)", output)
    loss_match = re.search(r"(\d+)% packet loss", output)
    
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

    if loss_match:
        stats["packet_loss"] = int(loss_match.group(1))
        
    return stats

def ping(host: str, count: int = 4, timeout: int = 2) -> Dict[str, Union[str, float, int, bool]]:
    """
    Ping a host and return basic statistics.
    
    :param host: The hostname or IP address to ping.
    :param count: Number of echo requests to send.
    :param timeout: Timeout in seconds for each ping/request.
    :return: A dict with success status and summary output.
    """
    
    system = platform.system()
    
    if system == "Windows":
        cmd = ["ping", "-n", str(count), "-w", str(timeout * 1000), host]
    else:  # Assuming Unix-like systems
        cmd = ["ping", "-c", str(count), "-W", str(timeout), host]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
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
        
async def async_ping(
    host: str,
    count: int = 4
) -> Dict[str, Union[str, float, int, bool]]:
    """
    Asynchronously ping a host and return basic statistics.

    :param host: The hostname or IP address to ping.
    :param count: Number of echo requests to send.
    :return: A dict with success status and summary output.
    """
    system = platform.system()
    # Use a default timeout value for the context manager
    timeout_seconds = 2
    if system == "Windows":
        cmd = ["ping", "-n", str(count), host]
    else:
        cmd = ["ping", "-c", str(count), host]
        
    try:
        async with asyncio.timeout(timeout_seconds):
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
    except asyncio.TimeoutError:
        return {
            "host": host,
            "success": False,
            "error": f"Ping timed out after {timeout_seconds} seconds",
            "raw_output": ""
        }
    except Exception as e:
        return {
            "host": host,
            "success": False,
            "error": str(e),
            "raw_output": ""
        }