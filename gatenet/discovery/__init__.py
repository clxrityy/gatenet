"""
Network discovery mechanisms for gatenet.

The discovery package contains passive and active techniques for
identifying devices and services on a local network. Each discovery
method is designed to be read-only and non-destructive.

Modules in this package may use different protocols (e.g. ARP, mDNS,
SSDP) but all return results using shared core models.
"""
