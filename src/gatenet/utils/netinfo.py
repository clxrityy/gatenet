"""
netinfo.py — Network interface and WiFi scanning utilities for gatenet.
"""
import socket
from typing import List, Dict, Optional

try:
    import psutil
except ImportError:
    psutil = None

# --- Interface Scanning ---
def list_network_interfaces() -> List[Dict[str, str]]:
    """
    List all network interfaces with their IP and MAC addresses.

    Returns
    -------
    List[Dict[str, str]]
        Each dict contains: name, ip, mac
    """
    interfaces = []
    if psutil:
        for name, addrs in psutil.net_if_addrs().items():
            iface = {"name": name, "ip": "", "mac": ""}
            for addr in addrs:
                if addr.family == socket.AF_INET:
                    iface["ip"] = addr.address
                elif addr.family == psutil.AF_LINK:
                    iface["mac"] = addr.address
            interfaces.append(iface)
    else:
        # Fallback: only list localhost
        interfaces.append({"name": "lo", "ip": "127.0.0.1", "mac": ""})
    return interfaces

# --- WiFi Scanning (macOS/Linux only) ---
def scan_wifi_networks(interface: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Scan for available WiFi networks (SSID, signal, security).
    Only works on macOS/Linux with 'airport' or 'iwlist'.

    Parameters
    ----------
    interface : Optional[str]
        Wireless interface name (default: autodetect)

    Returns
    -------
    List[Dict[str, str]]
        Each dict contains: ssid, signal, security
    """
    import platform

    system = platform.system()
    if system == "Darwin":
        return _scan_wifi_macos()
    elif system == "Linux":
        iface = interface or "wlan0"
        return _scan_wifi_linux(iface)
    else:
        return [{"error": "WiFi scan not supported on this OS"}]


def _scan_wifi_macos() -> List[Dict[str, str]]:
    import subprocess
    airport = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
    cmd = [airport, "-s"]
    try:
        output = subprocess.check_output(cmd, text=True)
        return _parse_macos_airport_output(output)
    except Exception as e:
        return [{"error": str(e)}]


def _get_col_ranges(header: str, columns: list) -> list:
    # Remove leading spaces for alignment
    leading = len(header) - len(header.lstrip())
    header_stripped = header.lstrip()
    col_starts = []
    for col in columns:
        idx = header_stripped.find(col)
        if idx != -1:
            col_starts.append((col, idx + leading))
    col_starts.sort(key=lambda x: x[1])
    col_ranges = []
    for i, (col, start) in enumerate(col_starts):
        end = col_starts[i+1][1] if i+1 < len(col_starts) else None
        col_ranges.append((col, start, end))
    return col_ranges

def _parse_airport_line(line: str, col_ranges: list) -> Dict[str, str]:
    # Find the minimum start index (indentation) from col_ranges
    min_start = min((start for _, start, _ in col_ranges), default=0)
    # Pad line with spaces if it is less indented than header
    leading = len(line) - len(line.lstrip())
    if leading < min_start:
        line = " " * (min_start - leading) + line
    fields = {}
    for col, start, end in col_ranges:
        val = line[start:end].strip() if end is not None else line[start:].strip()
        fields[col] = val
    return {
        "ssid": fields.get("SSID", ""),
        "signal": fields.get("RSSI", ""),
        "security": fields.get("SECURITY", "")
    }

def _parse_macos_airport_output(output: str) -> List[Dict[str, str]]:
    """
    Parse the output from the macOS 'airport -s' command.

    Parameters
    ----------
    output : str
        The raw output string from the airport command.

    Returns
    -------
    List[Dict[str, str]]
        Each dict contains: ssid, signal, security
    """
    results = []
    lines = output.splitlines()
    if not lines or len(lines) < 2:
        return results
    header = lines[0]
    columns = ["SSID", "BSSID", "RSSI", "CHANNEL", "HT", "CC", "SECURITY"]
    col_ranges = _get_col_ranges(header, columns)
    for line in lines[1:]:
        if line.strip():
            results.append(_parse_airport_line(line, col_ranges))
    return results


def _scan_wifi_linux(iface: str) -> List[Dict[str, str]]:
    import subprocess
    try:
        output = subprocess.check_output(
            ["iwlist", iface, "scan"], text=True, stderr=subprocess.DEVNULL
        )
        return _parse_linux_iwlist_output(output)
    except Exception as e:
        return [{"error": str(e)}]


def _parse_linux_iwlist_output(output: str) -> List[Dict[str, str]]:
    import re
    results = []
    for cell in re.split(r"Cell ", output)[1:]:
        ssid = re.search(r'ESSID:"([^"]+)"', cell)
        signal = re.search(r'Signal level=([\-\d]+)', cell)
        enc = re.search(r'Encryption key:(on|off)', cell)
        results.append({
            "ssid": ssid.group(1) if ssid else "",
            "signal": signal.group(1) if signal else "",
            "security": "WPA/WEP" if enc and enc.group(1) == "on" else "Open"
        })
    return results
