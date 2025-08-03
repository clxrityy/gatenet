"""
service_discovery.py
--------------------
Unified service discovery for multiple protocols (SNMP, LDAP, CoAP, MQTT, SIP, etc).

Provides a single ServiceDiscovery class for extensible protocol detection.
"""
from typing import Optional, Dict, List

class ServiceDiscovery:
    """
    Unified service discovery for multiple protocols.
    Register protocols with ports and banner keywords.

    Example:
        from gatenet.discovery.service_discovery import service_discovery
        result = service_discovery.detect(389, "LDAP server ready")
        if result:
            print(result["protocol"])  # Output: LDAP
    """
    def __init__(self):
        self.protocols: List[Dict] = []

    def register_protocol(self, name: str, ports: List[int], banner_keywords: List[str]):
        """
        Register a protocol for service discovery.

        Example:
            >>> sd = ServiceDiscovery()
            >>> sd.register_protocol("LDAP", [389], ["LDAP server ready"])
        """
        self.protocols.append({
            "name": name,
            "ports": set(ports),
            "banner_keywords": [kw.lower() for kw in banner_keywords]
        })

    def detect(self, port: int, banner: str) -> Optional[Dict]:
        """
        Detect the protocol based on port and banner.

        Example:
            >>> sd = ServiceDiscovery()
            >>> sd.register_protocol("LDAP", [389], ["LDAP server ready"])
            >>> result = sd.detect(389, "LDAP server ready")
            >>> print(result["protocol"])
        """
        banner_lc = (banner or "").lower()
        for proto in self.protocols:
            if port in proto["ports"] or any(kw in banner_lc for kw in proto["banner_keywords"]):
                return {
                    "protocol": proto["name"],
                    "port": port,
                    "banner": banner,
                    "detected": True
                }
        return None

# Pre-register common protocols
service_discovery = ServiceDiscovery()
service_discovery.register_protocol("SNMP", [161, 162], ["snmp"])
service_discovery.register_protocol("LDAP", [389], ["ldap"])
service_discovery.register_protocol("CoAP", [5683], ["coap"])
service_discovery.register_protocol("MQTT", [1883], ["mqtt"])
service_discovery.register_protocol("SIP", [5060], ["sip"])
