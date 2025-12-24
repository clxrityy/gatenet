from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Port:
    number: int
    protocol: str = "tcp"
    service: Optional[str] = None


@dataclass
class Service:
    name: str
    ports: List[Port]


@dataclass
class Device:
    ip: str
    hostname: Optional[str] = None
    services: List[Service] = field(default_factory=list)


@dataclass
class ScanResult:
    target: str
    open_ports: List[Port]
