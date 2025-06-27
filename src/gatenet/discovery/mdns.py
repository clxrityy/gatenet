from typing import List, Dict, Any
import time
from zeroconf import Zeroconf, ServiceBrowser, ServiceListener

class MDNSListener(ServiceListener):
    """Listener for mDNS service discovery."""
    
    def __init__(self) -> None:
        self.services: List[Dict[str, str]] = []
    
    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        """Called when a service is discovered."""
        try:
            info = zc.get_service_info(type_, name)
            if not info:
                return

            service_data = {
                "name": name,
                "type": type_,
                "address": str(info.parsed_addresses()[0]) if info.parsed_addresses() else "unknown",
                "port": str(info.port),
                "server": info.server if info.server else "unknown"
            }

            if info.properties:
                service_data["properties"] = str(self._decode_properties(info.properties))

            self.services.append(service_data)
        except Exception as e:
            # Log error but don't crash discovery
            print(f"Error processing service {name}: {e}")

    def _decode_properties(self, properties: Any) -> Dict[str, str]:
        """Helper to decode service properties."""
        decoded = {}
        for key, value in properties.items():
            try:
                key_str = key.decode('utf-8')
                if value is None:
                    decoded[key_str] = ""
                elif isinstance(value, bytes):
                    decoded[key_str] = value.decode('utf-8')
                else:
                    decoded[key_str] = str(value)
            except (UnicodeDecodeError, AttributeError):
                continue
        return decoded
    
    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        """Called when a service is removed."""
        pass
    
    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        """Called when a service is updated."""
        pass

def discover_mdns_services(timeout: float = 2.0) -> List[Dict[str, str]]:
    """
    Discover mDNS / Bonjour services on the local network.
    
    :param timeout: Time (in seconds) to wait for responses.
    :return: List of discovered services.
    """
    zeroconf = None
    try:
        zeroconf = Zeroconf()
        listener = MDNSListener()
        _ = ServiceBrowser(zeroconf, "_services._dns-sd._udp.local.", listener)
        
        time.sleep(timeout)  # Allow time for discovery
        
        return listener.services
    except Exception as e:
        print(f"Error during mDNS discovery: {e}")
        return []
    finally:
        if zeroconf:
            zeroconf.close()