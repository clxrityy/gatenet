"""
DHCP server management for hotspot functionality.
"""
import subprocess
import platform
from typing import Optional


class DHCPServer:
    """
    Manage DHCP server for hotspot clients.
    
    Example:
        >>> from gatenet.hotspot import DHCPServer
        >>> dhcp = DHCPServer("192.168.4.0/24", "192.168.4.1")
        >>> dhcp.start()
        >>> dhcp.stop()
    """
    
    def __init__(self, ip_range: str, gateway: str, dns_servers: Optional[list] = None):
        self.ip_range = ip_range
        self.gateway = gateway
        self.dns_servers = dns_servers or ["8.8.8.8", "8.8.4.4"]
        self.is_running = False
        self.system = platform.system()
        
    def start(self) -> bool:
        """
        Start the DHCP server.
        
        Returns:
            bool: True if started successfully, False otherwise
        """
        try:
            if self.system == "Linux":
                return self._start_dnsmasq()
            elif self.system == "Darwin":
                return self._start_macos_dhcp()
            else:
                return False
        except Exception as e:
            print(f"Error starting DHCP server: {e}")
            return False
    
    def stop(self) -> bool:
        """
        Stop the DHCP server.
        
        Returns:
            bool: True if stopped successfully, False otherwise
        """
        try:
            if self.system == "Linux":
                return self._stop_dnsmasq()
            elif self.system == "Darwin":
                return self._stop_macos_dhcp()
            else:
                return False
        except Exception as e:
            print(f"Error stopping DHCP server: {e}")
            return False
    
    def _start_dnsmasq(self) -> bool:
        """Start dnsmasq DHCP server on Linux."""
        # Extract network info
        network_parts = self.ip_range.split('/')
        network = network_parts[0]
        
        # Calculate DHCP range
        base_ip = ".".join(network.split('.')[:-1])
        start_ip = f"{base_ip}.10"
        end_ip = f"{base_ip}.100"
        
        # Create dnsmasq config
        config = f"""
interface=wlan0
dhcp-range={start_ip},{end_ip},255.255.255.0,24h
dhcp-option=3,{self.gateway}
dhcp-option=6,{','.join(self.dns_servers)}
"""
        
        # Write config
        with open("/tmp/dnsmasq.conf", "w") as f:
            f.write(config)
        
        # Start dnsmasq
        result = subprocess.run(["sudo", "dnsmasq", "-C", "/tmp/dnsmasq.conf"], 
                              capture_output=True, text=True, check=False)
        
        if result.returncode == 0:
            self.is_running = True
            return True
        return False
    
    def _stop_dnsmasq(self) -> bool:
        """Stop dnsmasq DHCP server."""
        try:
            subprocess.run(["sudo", "pkill", "dnsmasq"], check=False)
            self.is_running = False
            return True
        except Exception:
            return False
    
    def _start_macos_dhcp(self) -> bool:
        """Start DHCP server on macOS."""
        # macOS uses built-in DHCP when Internet Sharing is enabled
        # This is typically handled by the system
        self.is_running = True
        return True
    
    def _stop_macos_dhcp(self) -> bool:
        """Stop DHCP server on macOS."""
        self.is_running = False
        return True
