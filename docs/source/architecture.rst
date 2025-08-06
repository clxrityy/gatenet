.. _architecture:

Gatenet Architecture
====================




.. mermaid::

   flowchart TD
     Gatenet
     Gatenet --> diagnostics
     Gatenet --> client
     Gatenet --> http_
     Gatenet --> socket
     Gatenet --> discovery
     Gatenet --> service_detectors
     Gatenet --> mesh
     Gatenet --> radio
     Gatenet --> hotspot
     Gatenet --> cli



Gatenet Core Modules
--------------------

**cli/**
    Modular command-line interface for diagnostics, service discovery, and network utilities. Provides colorized output, robust error handling, and extensible command structure. Integrates with all core modules using only internal APIs.

**diagnostics/**
    Network diagnostics tools: DNS, geo IP, ping, port scanning, bandwidth measurement, and more. Provides both sync and async APIs for robust network testing.

**client/**
    TCP and UDP client implementations, including base classes for extensibility. Supports both synchronous and asynchronous communication.

**http_/**
    HTTP server and client modules, including async support. Built on Python stdlib and aiohttp. Enables RESTful APIs, microservices, and webhooks.

**socket/**
    Low-level TCP and UDP socket servers and base classes. Designed for extensibility and robust connection handling.

**discovery/**
    Service discovery modules: mDNS, UPNP, SSH, Bluetooth, and a unified service_discovery interface. Implements strategy and chain-of-responsibility patterns.

**service_detectors/**
    Extensible protocol and service detection classes (e.g., SSHDetector, HTTPDetector, IMAPDetector, etc.). Supports custom detectors and fluent chaining for advanced service identification.

**mesh/**
    Modular mesh networking and radio interface. Includes MeshRadio (base), LoRaRadio, and ESPRadio for encrypted messaging, packet parsing, and topology mapping. Designed for extensibility and protocol-specific features. Supports both simulation and hardware integration.

**radio/**
    Standalone radio frequency (RF) detection and integration module. Provides SDR, LoRa, and ESP classes for frequency scanning, signal decoding, event-driven callbacks, and seamless mesh integration. Supports hardware and simulation, GPS tagging, and extensible event handling for RF signals.

**hotspot/**
    Wi-Fi access point creation and management module. Provides cross-platform hotspot creation with comprehensive security configuration (WPA2, WPA3, WEP, Open). Includes integrated DHCP server management, real-time device monitoring, and robust password generation. Supports Linux (hostapd/dnsmasq) and macOS (Internet Sharing) with automated network configuration.

Each module is modular, extensible, and well-tested. See the API reference for details on each submodule and class.
