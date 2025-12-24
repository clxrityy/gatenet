from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Port:
    """
    Represents a network port exposed by a service.

    Attributes:
        number (int): Port number.
        protocol (str): Transport protocol (e.g. 'tcp', 'udp').
        service (Optional[str]): Known service name, if identified.
    """
    number: int
    protocol: str = "tcp"
    service: Optional[str] = None


@dataclass
class Service:
    """
    Represents a network service running on a device.

    Attributes:
        name (str): Human-readable service name.
        ports (List[Port]): Ports associated with this service.
    """
    name: str
    ports: List[Port]


@dataclass
class Device:
    """
    Represents a network-connected device.

    Attributes:
        ip (str): IPv4 or IPv6 address.
        hostname (Optional[str]): Resolved hostname, if available.
        services (List[Service]): Discovered services on the device.
    """
    ip: str
    hostname: Optional[str] = None
    services: List[Service] = field(default_factory=list)


@dataclass
class ScanResult:
    """
    Represents the result of a port scan.

    Attributes:
        target (str): Scan target (IP, hostname, or CIDR).
        open_ports (List[Port]): Open ports discovered on the target.
    """
    target: str
    open_ports: List[Port]