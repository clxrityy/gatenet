"""
Gatenet discovery module.

Provides service discovery functionality including mDNS, UPnP, Bluetooth,
and various service detection strategies.
"""

from .mdns import discover_mdns_services, MDNSListener
from .upnp import discover_upnp_devices

# Bluetooth imports - optional dependency
try:
    from .bluetooth import async_discover_bluetooth_devices, discover_bluetooth_devices
    _BLUETOOTH_AVAILABLE = True
except ImportError:
    from typing import Dict, List
    _BLUETOOTH_AVAILABLE = False
    # Create stub functions for when bleak is not available
    def discover_bluetooth_devices(timeout: float = 8.0) -> List[Dict[str, str]]:
        """Bluetooth discovery is not available. Install with: pip install gatenet[bluetooth]"""
        raise ImportError("Bluetooth discovery requires 'bleak' package. Install with: pip install gatenet[bluetooth]")
    
    async def async_discover_bluetooth_devices() -> List[Dict[str, str]]:
        """Bluetooth discovery is not available. Install with: pip install gatenet[bluetooth]"""
        raise ImportError("Bluetooth discovery requires 'bleak' package. Install with: pip install gatenet[bluetooth]")

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