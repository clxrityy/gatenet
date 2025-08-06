"""
Gatenet diagnostics module.

Provides networking diagnostic tools including ping, traceroute, DNS lookups,
port scanning, geolocation, and bandwidth testing.
"""

from .dns import reverse_dns_lookup, dns_lookup
from .port_scan import check_public_port, scan_ports, check_port, scan_ports_async
from .geo import get_geo_info
from .ping import ping, async_ping, ping_with_rf
from .traceroute import traceroute

# Import bandwidth if available (may have optional dependencies)
try:
    from .bandwidth import measure_bandwidth
except ImportError:
    measure_bandwidth = None

__all__ = [
    "reverse_dns_lookup",
    "dns_lookup", 
    "check_public_port",
    "scan_ports",
    "check_port",
    "scan_ports_async",
    "get_geo_info",
    "ping",
    "async_ping",
    "ping_with_rf",
    "traceroute",
    "measure_bandwidth",
]