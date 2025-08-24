"""
Gatenet - A modular Python networking toolkit for diagnostics, service discovery, and robust socket/HTTP microservices.

Gatenet is designed for extensibility, testability, and modern async support.

Example usage:
    >>> from gatenet.client.tcp import TCPClient
    >>> from gatenet.diagnostics.ping import ping
    >>> from gatenet.discovery.ssh import SSHDetector
    >>> from gatenet.http_.client import HTTPClient
"""

__version__ = "0.12.6"
__author__ = "MJ Anglin"
__email__ = "contact@mjanglin.com"

# Import main modules to make them available at package level
from . import client
from . import diagnostics
from . import discovery
from . import http_
from . import socket
from . import utils
from . import core

# Import optional modules if available
try:
    from . import dashboard
except ImportError:
    dashboard = None

try:
    from . import mesh
except ImportError:
    mesh = None

try:
    from . import radio
except ImportError:
    radio = None

try:
    from . import hotspot
except ImportError:
    hotspot = None

try:
    from . import service_detectors
except ImportError:
    service_detectors = None

# Import CLI if available
try:
    from . import cli
except ImportError:
    # CLI might not be available in all installations
    cli = None

__all__ = [
    "client",
    "diagnostics", 
    "discovery",
    "http_",
    "socket",
    "utils",
    "cli",
    "dashboard",
    "mesh",
    "radio",
    "hotspot",
    "service_detectors",
    "core"
]
