"""
Main hotspot management class for creating and controlling Wi-Fi access points.
"""
import subprocess
import platform
import time
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
import tempfile
import os
from .security import SecurityConfig
from .dhcp import DHCPServer
from .backend import HotspotBackend, BackendResult


@dataclass
class HotspotConfig:
    """Configuration for hotspot creation."""
    ssid: str
    password: Optional[str] = None
    interface: str = "wlan0"
    ip_range: str = "192.168.4.0/24"
    gateway: str = "192.168.4.1"
    channel: int = 6
    hidden: bool = False


class Hotspot:
    """
    Create and manage Wi-Fi hotspots on Linux/macOS systems.
    
    Example:
        >>> from gatenet.hotspot import Hotspot, HotspotConfig
        >>> config = HotspotConfig(ssid="MyHotspot", password="mypassword123")
        >>> hotspot = Hotspot(config)
        >>> hotspot.start()
        >>> hotspot.get_connected_devices()
        >>> hotspot.stop()
    """
    
    def __init__(self, config: HotspotConfig, backend: Optional[HotspotBackend] = None):
        self.config = config
        self.security = SecurityConfig(config.password) if config.password else None
        self.dhcp_server = DHCPServer(config.ip_range, config.gateway)
        self.is_running = False
        self.system = platform.system()
        self._backend = backend  # allow injection for tests or custom platforms
        
    def start(self) -> bool:
        """
        Start the hotspot.
        
        Returns:
            bool: True if started successfully, False otherwise
            
        Example:
            >>> hotspot = Hotspot(HotspotConfig("TestHotspot", "password123"))
            >>> success = hotspot.start()
        """
        try:
            if self._backend:
                result: BackendResult = self._backend.start()
                self.is_running = result.ok
                return result.ok
            if self.system == "Linux":
                return self._start_linux()
            elif self.system == "Darwin":
                return self._start_macos()
            else:
                raise NotImplementedError(f"Hotspot not supported on {self.system}")
        except Exception as e:
            print(f"Error starting hotspot: {e}")
            return False
    
    def stop(self) -> bool:
        """
        Stop the hotspot.
        
        Returns:
            bool: True if stopped successfully, False otherwise
        """
        try:
            if self._backend:
                result: BackendResult = self._backend.stop()
                self.is_running = not result.ok and self.is_running
                return result.ok
            if self.system == "Linux":
                return self._stop_linux()
            elif self.system == "Darwin":
                return self._stop_macos()
            else:
                return False
        except Exception as e:
            print(f"Error stopping hotspot: {e}")
            return False
    
    def get_connected_devices(self) -> List[Dict[str, str]]:
        """
        Get list of devices connected to the hotspot.
        
        Returns:
            List[Dict]: List of connected devices with MAC, IP, and hostname
            
        Example:
            >>> devices = hotspot.get_connected_devices()
            >>> print(f"Connected devices: {len(devices)}")
        """
        if not self.is_running:
            return []
            
        try:
            if self._backend:
                return self._backend.devices()
            if self.system == "Linux":
                return self._get_devices_linux()
            elif self.system == "Darwin":
                return self._get_devices_macos()
            else:
                return []
        except Exception:
            return []
    
    def _start_linux(self) -> bool:
        """Start hotspot on Linux using hostapd and dnsmasq."""
        # Create hostapd configuration
        hostapd_conf = f"""
interface={self.config.interface}
driver=nl80211
ssid={self.config.ssid}
hw_mode=g
channel={self.config.channel}
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid={1 if self.config.hidden else 0}
"""
        
        if self.security:
            hostapd_conf += f"""
wpa=2
wpa_passphrase={self.config.password}
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
"""
        
        # Write hostapd config securely using a temporary file
        with tempfile.NamedTemporaryFile("w", delete=False, prefix="hostapd_", suffix=".conf") as tmpfile:
            tmpfile.write(hostapd_conf)
            hostapd_conf_path = tmpfile.name
        
        try:
            # Configure interface
            subprocess.run(["sudo", "ip", "addr", "add", f"{self.config.gateway}/24", "dev", self.config.interface], check=False)
            subprocess.run(["sudo", "ip", "link", "set", self.config.interface, "up"], check=False)
        
            # Start DHCP server
            self.dhcp_server.start()
        
            # Start hostapd
            result = subprocess.run(["sudo", "hostapd", hostapd_conf_path], 
                                  capture_output=True, text=True, check=False)
        
            if result.returncode == 0:
                self.is_running = True
                return True
            return False
        finally:
            # Remove the temporary config file securely
            if os.path.exists(hostapd_conf_path):
                try:
                    os.remove(hostapd_conf_path)
                except Exception:
                    pass
    
    def _start_macos(self) -> bool:
        """Start hotspot on macOS using built-in sharing."""
        # Note: macOS requires manual configuration in System Preferences
        # This is a simplified approach using networksetup
        try:
            # Enable Internet Sharing (requires manual setup in System Preferences)
            subprocess.run(["sudo", "launchctl", "load", "-w", 
                          "/System/Library/LaunchDaemons/com.apple.InternetSharing.plist"], 
                          check=False)
            self.is_running = True
            return True
        except Exception:
            return False
    
    def _stop_linux(self) -> bool:
        """Stop hotspot on Linux."""
        try:
            # Stop hostapd
            subprocess.run(["sudo", "pkill", "hostapd"], check=False)
            
            # Stop DHCP server
            self.dhcp_server.stop()
            
            # Reset interface
            subprocess.run(["sudo", "ip", "link", "set", self.config.interface, "down"], check=False)
            subprocess.run(["sudo", "ip", "addr", "flush", "dev", self.config.interface], check=False)
            
            self.is_running = False
            return True
        except Exception:
            return False
    
    def _stop_macos(self) -> bool:
        """Stop hotspot on macOS."""
        try:
            subprocess.run(["sudo", "launchctl", "unload", "-w", 
                          "/System/Library/LaunchDaemons/com.apple.InternetSharing.plist"], 
                          check=False)
            self.is_running = False
            return True
        except Exception:
            return False
    
    def _get_devices_linux(self) -> List[Dict[str, str]]:
        """Get connected devices on Linux using ARP table."""
        devices = []
        try:
            # Get ARP table
            result = subprocess.run(["arp", "-a"], capture_output=True, text=True, check=False)
            for line in result.stdout.split('\n'):
                if self.config.gateway.split('.')[:-1] == line.split()[-1].strip('()').split('.')[:-1]:
                    parts = line.split()
                    if len(parts) >= 4:
                        hostname = parts[0]
                        ip = parts[1].strip('()')
                        mac = parts[3]
                        devices.append({"hostname": hostname, "ip": ip, "mac": mac})
        except Exception:
            pass
        return devices
    
    def _get_devices_macos(self) -> List[Dict[str, str]]:
        """Get connected devices on macOS."""
        # Similar to Linux, but may need different parsing
        return self._get_devices_linux()
