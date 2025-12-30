"""Core data models used throughout gatenet.

This module defines lightweight, immutable-by-convention data structures
that represent network entities such as devices, services, ports, and scan
results. These models are shared across discovery, scanning, and reporting
layers to ensure a consistent internal representation.

The models are intentionally simple and contain no networking logic.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Port:
    """Represents a network port exposed by a device or service.

    A Port describes the transport-level endpoint and any known service
    metadata associated with it. It does not imply that the port is open
    unless explicitly returned by a scan result.

    Attributes:
        number: The port number (1–65535).
        protocol: Transport protocol used by the port (e.g. "tcp", "udp").
        service: Optional well-known or inferred service name.
    """

    number: int
    protocol: str = "tcp"
    service: Optional[str] = None


@dataclass
class Service:
    """Represents a logical network service.

    A Service groups one or more ports under a single human-readable name.
    This is useful for higher-level discovery layers (e.g. mDNS, UPnP)
    where services may span multiple ports.

    Attributes:
        name: Human-readable service name.
        ports: Ports associated with this service.
    """

    name: str
    ports: List[Port]


@dataclass
class Device:
    """Represents a network-connected device.

    A Device aggregates identity information (IP, hostname) along with any
    discovered services. It may be partially populated depending on the
    discovery or scanning method used.

    Attributes:
        ip: IPv4 or IPv6 address of the device.
        hostname: Resolved hostname, if available.
        services: Services discovered on the device.
    """

    ip: str
    hostname: Optional[str] = None
    services: List[Service] = field(default_factory=list)


@dataclass
class ScanResult:
    """Represents the result of a network scan operation.

    ScanResult captures the outcome of scanning a single target, including
    any open ports that were identified. It is intended to be a read-only
    snapshot of scan state.

    Attributes:
        target: Scan target (IP address, hostname, or CIDR range).
        open_ports: Open ports discovered on the target.
    """

    target: str
    open_ports: List[Port]
