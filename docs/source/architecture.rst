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

Each module is modular, extensible, and well-tested. See the API reference for details on each submodule and class.
