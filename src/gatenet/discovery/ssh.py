from typing import Optional, Iterable, List
from gatenet.core import hooks, events
from .detectors import (
    ServiceDetector,
    SSHDetector,
    HTTPDetector,
    FTPDetector,
    SMTPDetector,
    PortMappingDetector,
    BannerKeywordDetector,
    GenericServiceDetector,
    FallbackDetector,
)

_REGISTRY: List[ServiceDetector] = [
    SSHDetector(),
    HTTPDetector(), 
    FTPDetector(),
    SMTPDetector(),
    PortMappingDetector(),
    BannerKeywordDetector(),
    GenericServiceDetector(),
    FallbackDetector(),  # Always returns a result
]

def register_detector(detector: ServiceDetector, *, append: bool = True) -> None:
    """Register a custom service detector.

    Parameters
    ----------
    detector : ServiceDetector
        The detector instance to add to the chain.
    append : bool, optional
        If True, add to the end; if False, insert near the beginning (after SSH/HTTP).
    """
    if append:
        # Keep fallback last
        fallback = _REGISTRY.pop() if _REGISTRY and isinstance(_REGISTRY[-1], FallbackDetector) else None
        _REGISTRY.append(detector)
        if fallback:
            _REGISTRY.append(fallback)
    else:
        insert_idx = 2  # after SSH, HTTP
        _REGISTRY.insert(insert_idx, detector)

def register_detectors(detectors: Iterable[ServiceDetector]) -> None:
    for d in detectors:
        register_detector(d)

def clear_detectors(keep_defaults: bool = True) -> None:
    """Clear the registry.

    If keep_defaults is True, restore built-ins; otherwise leave empty.
    """
    global _REGISTRY
    if keep_defaults:
        _REGISTRY = [
            SSHDetector(),
            HTTPDetector(),
            FTPDetector(),
            SMTPDetector(),
            PortMappingDetector(),
            BannerKeywordDetector(),
            GenericServiceDetector(),
            FallbackDetector(),
        ]
    else:
        _REGISTRY = []

def get_detectors() -> List[ServiceDetector]:
    return list(_REGISTRY)

def _identify_service(port: int, banner: str) -> str:
    """
    Identify service type from port and banner.

    Parameters
    ----------
    port : int
        Port number where the service is running.
    banner : str
        Banner text received from the service.

    Returns
    -------
    str
        Identified service name and version.

    Example
    -------
    >>> from gatenet.discovery.ssh import _identify_service
    >>> _identify_service(22, "SSH-2.0-OpenSSH_8.9p1")
    'OpenSSH 8.9p1'
    """
    # Defensive: handle None or non-str banner
    if banner is None:
        banner_lower = ""
    elif not isinstance(banner, str):
        banner_lower = str(banner).lower().strip()
    else:
        banner_lower = banner.lower().strip()

    # Defensive: handle non-int port
    try:
        port_int = int(port)
    except Exception:
        port_int = -1

    # Emit before-detect hook
    try:
        hooks.emit(events.DISCOVERY_BEFORE_DETECT, port=port_int, banner=banner_lower)
    except Exception:
        pass

    # Chain of responsibility pattern using the registry
    for detector in get_detectors():
        result = detector.detect(port_int, banner_lower)
        if result:
            try:
                hooks.emit(events.DISCOVERY_AFTER_DETECT, port=port_int, banner=banner_lower, result=result)
            except Exception:
                pass
            return result

    # This should never be reached due to FallbackDetector
    result = f"Unknown Service (Port {port_int})"
    try:
        hooks.emit(events.DISCOVERY_AFTER_DETECT, port=port_int, banner=banner_lower, result=result)
    except Exception:
        pass
    return result