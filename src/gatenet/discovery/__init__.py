"""
Gatenet discovery module.

Provides service discovery functionality including mDNS, UPnP, Bluetooth,
and various service detection strategies.
"""

from .mdns import discover_mdns_services, MDNSListener
from .upnp import discover_upnp_devices
from .bluetooth import async_discover_bluetooth_devices, discover_bluetooth_devices
from .ssh import (
    SSHDetector,
    ServiceDetector,
    register_detector,
    register_detectors,
    clear_detectors,
    get_detectors,
)
from .detectors import (
    HTTPDetector,
    FTPDetector,
    SMTPDetector,
    PortMappingDetector,
    BannerKeywordDetector,
    GenericServiceDetector,
    FallbackDetector,
)

__all__ = [
    "discover_mdns_services",
    "MDNSListener",
    "discover_upnp_devices", 
    "async_discover_bluetooth_devices",
    "discover_bluetooth_devices",
    "SSHDetector",
    "ServiceDetector",
    "HTTPDetector",
    "FTPDetector",
    "SMTPDetector",
    "PortMappingDetector",
    "BannerKeywordDetector",
    "GenericServiceDetector",
    "FallbackDetector",
    "register_detector",
    "register_detectors",
    "clear_detectors",
    "get_detectors",
]