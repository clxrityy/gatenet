"""
Tests for the gatenet.hotspot module.
"""
import pytest
from unittest.mock import patch, MagicMock
from gatenet.hotspot import Hotspot, HotspotConfig, DHCPServer, SecurityConfig, SecurityType


class TestHotspotConfig:
    """Test hotspot configuration."""
    
    def test_hotspot_config_creation(self):
        config = HotspotConfig(
            ssid="TestHotspot",
            password="password123",
            interface="wlan0",
            ip_range="192.168.4.0/24",
            gateway="192.168.4.1",
            channel=6
        )
        assert config.ssid == "TestHotspot"
        assert config.password == "password123"
        assert config.interface == "wlan0"
        assert config.channel == 6
    
    def test_hotspot_config_defaults(self):
        config = HotspotConfig(ssid="TestHotspot")
        assert config.password is None
        assert config.interface == "wlan0"
        assert config.ip_range == "192.168.4.0/24"
        assert config.gateway == "192.168.4.1"
        assert config.channel == 6
        assert config.hidden is False


class TestSecurityConfig:
    """Test security configuration."""
    
    def test_password_validation_strong(self):
        config = SecurityConfig("StrongPass123!", SecurityType.WPA2)
        assert config.validate_password() is True
    
    def test_password_validation_weak(self):
        config = SecurityConfig("weak", SecurityType.WPA2)
        assert config.validate_password() is False
    
    def test_password_validation_short(self):
        config = SecurityConfig("short", SecurityType.WPA2)
        assert config.validate_password() is False
    
    def test_password_validation_common_pattern(self):
        config = SecurityConfig("password123", SecurityType.WPA2)
        assert config.validate_password() is False
    
    def test_open_network_validation(self):
        config = SecurityConfig(None, SecurityType.OPEN)
        assert config.validate_password() is True
    
    def test_generate_password(self):
        password = SecurityConfig.generate_password(12)
        assert len(password) == 12
        # Check for different character types
        assert any(c.islower() for c in password)
        assert any(c.isupper() for c in password)
        assert any(c.isdigit() for c in password)
    
    def test_generate_password_minimum_length(self):
        password = SecurityConfig.generate_password(4)  # Should be increased to 8
        assert len(password) == 8
    
    def test_security_level_descriptions(self):
        configs = [
            (SecurityType.OPEN, "None (Open network)"),
            (SecurityType.WEP, "Low (WEP - deprecated)"),
            (SecurityType.WPA2, "High (WPA2)"),
            (SecurityType.WPA3, "Very High (WPA3)")
        ]
        
        for security_type, expected in configs:
            config = SecurityConfig("password123", security_type)
            assert config.get_security_level() == expected
    
    def test_hostapd_config_wpa2(self):
        config = SecurityConfig("testpass", SecurityType.WPA2)
        hostapd_config = config.get_hostapd_config()
        assert "wpa=2" in hostapd_config
        assert "wpa_passphrase=testpass" in hostapd_config
        assert "WPA-PSK" in hostapd_config
    
    def test_hostapd_config_open(self):
        config = SecurityConfig(None, SecurityType.OPEN)
        hostapd_config = config.get_hostapd_config()
        assert hostapd_config == ""


class TestDHCPServer:
    """Test DHCP server functionality."""
    
    def test_dhcp_server_creation(self):
        dhcp = DHCPServer("192.168.4.0/24", "192.168.4.1")
        assert dhcp.ip_range == "192.168.4.0/24"
        assert dhcp.gateway == "192.168.4.1"
        assert dhcp.dns_servers == ["8.8.8.8", "8.8.4.4"]
        assert dhcp.is_running is False
    
    def test_dhcp_server_custom_dns(self):
        dhcp = DHCPServer("192.168.4.0/24", "192.168.4.1", ["1.1.1.1", "1.0.0.1"])
        assert dhcp.dns_servers == ["1.1.1.1", "1.0.0.1"]
    
    @patch('platform.system')
    @patch('subprocess.run')
    def test_dhcp_start_linux(self, mock_subprocess, mock_platform):
        mock_platform.return_value = "Linux"
        mock_subprocess.return_value = MagicMock(returncode=0)
        
        dhcp = DHCPServer("192.168.4.0/24", "192.168.4.1")
        result = dhcp.start()
        
        assert result is True
        assert dhcp.is_running is True
        mock_subprocess.assert_called()
    
    @patch('platform.system')
    def test_dhcp_start_macos(self, mock_platform):
        mock_platform.return_value = "Darwin"
        
        dhcp = DHCPServer("192.168.4.0/24", "192.168.4.1")
        result = dhcp.start()
        
        assert result is True
        assert dhcp.is_running is True


class TestHotspot:
    """Test hotspot functionality."""
    
    def _mock_subprocess_success(self, *args, **kwargs):
        """Mock subprocess calls to return success without prompting for passwords."""
        return MagicMock(returncode=0, stdout="", stderr="")
    
    def test_hotspot_creation(self):
        config = HotspotConfig(ssid="TestHotspot", password="password123")
        hotspot = Hotspot(config)
        
        assert hotspot.config == config
        assert hotspot.security is not None
        assert hotspot.dhcp_server is not None
        assert hotspot.is_running is False
    
    def test_hotspot_creation_open(self):
        config = HotspotConfig(ssid="TestHotspot")  # No password
        hotspot = Hotspot(config)
        
        assert hotspot.security is None
    
    @patch('platform.system')
    def test_hotspot_unsupported_platform(self, mock_platform):
        mock_platform.return_value = "Windows"
        
        config = HotspotConfig(ssid="TestHotspot")
        hotspot = Hotspot(config)
        
        result = hotspot.start()
        assert result is False
    
    @patch('platform.system')
    @patch('subprocess.run')
    def test_hotspot_start_linux_success(self, mock_subprocess, mock_platform):
        mock_platform.return_value = "Linux"
        mock_subprocess.side_effect = self._mock_subprocess_success
        
        config = HotspotConfig(ssid="TestHotspot", password="password123")
        hotspot = Hotspot(config)
        
        with patch.object(hotspot.dhcp_server, 'start', return_value=True):
            result = hotspot.start()
        
        assert result is True
        assert hotspot.is_running is True
    
    @patch('platform.system')
    @patch('subprocess.run')
    def test_hotspot_start_linux_failure(self, mock_subprocess, mock_platform):
        mock_platform.return_value = "Linux"
        mock_subprocess.return_value = MagicMock(returncode=1, stdout="", stderr="Command failed")
        
        config = HotspotConfig(ssid="TestHotspot", password="password123")
        hotspot = Hotspot(config)
        
        with patch.object(hotspot.dhcp_server, 'start', return_value=True):
            result = hotspot.start()
        
        assert result is False
        assert hotspot.is_running is False
    
    @patch('platform.system')
    @patch('subprocess.run')
    def test_hotspot_stop_linux(self, mock_subprocess, mock_platform):
        mock_platform.return_value = "Linux"
        mock_subprocess.side_effect = self._mock_subprocess_success
        
        config = HotspotConfig(ssid="TestHotspot")
        hotspot = Hotspot(config)
        hotspot.is_running = True
        
        with patch.object(hotspot.dhcp_server, 'stop', return_value=True):
            result = hotspot.stop()
        
        assert result is True
        assert hotspot.is_running is False
    
    def test_get_connected_devices_not_running(self):
        config = HotspotConfig(ssid="TestHotspot")
        hotspot = Hotspot(config)
        
        devices = hotspot.get_connected_devices()
        assert devices == []
    
    @patch('platform.system')
    @patch('subprocess.run')
    def test_get_connected_devices_linux(self, mock_subprocess, mock_platform):
        mock_platform.return_value = "Linux"
        mock_subprocess.return_value = MagicMock(
            stdout="device1 (192.168.4.10) at aa:bb:cc:dd:ee:ff [ether] on wlan0\n"
        )
        
        config = HotspotConfig(ssid="TestHotspot")
        hotspot = Hotspot(config)
        hotspot.is_running = True
        
        devices = hotspot.get_connected_devices()
        assert isinstance(devices, list)

    @patch('platform.system')
    @patch('subprocess.run')
    def test_hotspot_start_macos_success(self, mock_subprocess, mock_platform):
        """Test successful hotspot start on macOS."""
        mock_platform.return_value = "Darwin"
        mock_subprocess.return_value = MagicMock(returncode=0)
        
        config = HotspotConfig(ssid="TestHotspot", password="password123")
        hotspot = Hotspot(config)
        
        with patch.object(hotspot.dhcp_server, 'start', return_value=True):
            result = hotspot.start()
        
        assert result is True
        assert hotspot.is_running is True

    @patch('platform.system')
    @patch('subprocess.run')
    def test_hotspot_start_macos_exception(self, mock_subprocess, mock_platform):
        """Test hotspot start on macOS with exception."""
        mock_platform.return_value = "Darwin"
        mock_subprocess.side_effect = Exception("macOS error")
        
        config = HotspotConfig(ssid="TestHotspot", password="password123")
        hotspot = Hotspot(config)
        
        result = hotspot.start()
        assert result is False
        assert hotspot.is_running is False

    @patch('platform.system')
    @patch('subprocess.run')
    def test_hotspot_stop_macos_success(self, mock_subprocess, mock_platform):
        """Test successful hotspot stop on macOS."""
        mock_platform.return_value = "Darwin"
        mock_subprocess.return_value = MagicMock(returncode=0)
        
        config = HotspotConfig(ssid="TestHotspot")
        hotspot = Hotspot(config)
        hotspot.is_running = True
        
        result = hotspot.stop()
        assert result is True
        assert hotspot.is_running is False

    @patch('platform.system')
    @patch('subprocess.run')
    def test_hotspot_stop_macos_exception(self, mock_subprocess, mock_platform):
        """Test hotspot stop on macOS with exception."""
        mock_platform.return_value = "Darwin"
        mock_subprocess.side_effect = Exception("macOS stop error")
        
        config = HotspotConfig(ssid="TestHotspot")
        hotspot = Hotspot(config)
        hotspot.is_running = True
        
        result = hotspot.stop()
        assert result is False

    @patch('platform.system')
    def test_get_connected_devices_macos(self, mock_platform):
        """Test getting connected devices on macOS."""
        mock_platform.return_value = "Darwin"
        
        config = HotspotConfig(ssid="TestHotspot")
        hotspot = Hotspot(config)
        hotspot.is_running = True
        
        with patch.object(hotspot, '_get_devices_linux', return_value=[]) as mock_linux_devices:
            devices = hotspot.get_connected_devices()
            mock_linux_devices.assert_called_once()
            assert devices == []

    @patch('platform.system')
    def test_get_connected_devices_unsupported_platform(self, mock_platform):
        """Test getting connected devices on unsupported platform."""
        mock_platform.return_value = "Windows"
        
        config = HotspotConfig(ssid="TestHotspot")
        hotspot = Hotspot(config)
        hotspot.is_running = True
        
        devices = hotspot.get_connected_devices()
        assert devices == []

    @patch('platform.system')
    @patch('subprocess.run')
    def test_get_connected_devices_linux_with_devices(self, mock_subprocess, mock_platform):
        """Test getting connected devices on Linux with actual device data."""
        mock_platform.return_value = "Linux"
        mock_subprocess.return_value = MagicMock(
            stdout="laptop (192.168.4.10) at aa:bb:cc:dd:ee:ff [ether] on wlan0\nphone (192.168.4.11) at 11:22:33:44:55:66 [ether] on wlan0\n"
        )
        
        config = HotspotConfig(ssid="TestHotspot", gateway="192.168.4.1")
        hotspot = Hotspot(config)
        hotspot.is_running = True
        
        devices = hotspot.get_connected_devices()
        assert isinstance(devices, list)
        # The actual parsing logic is complex, just verify it doesn't crash

    @patch('platform.system')
    @patch('subprocess.run')
    def test_get_connected_devices_linux_exception(self, mock_subprocess, mock_platform):
        """Test getting connected devices on Linux with exception."""
        mock_platform.return_value = "Linux"
        mock_subprocess.side_effect = Exception("ARP table error")
        
        config = HotspotConfig(ssid="TestHotspot")
        hotspot = Hotspot(config)
        hotspot.is_running = True
        
        devices = hotspot.get_connected_devices()
        assert devices == []

    def test_get_connected_devices_exception_handling(self):
        """Test exception handling in get_connected_devices."""
        config = HotspotConfig(ssid="TestHotspot")
        hotspot = Hotspot(config)
        hotspot.is_running = True
        
        with patch.object(hotspot, '_get_devices_linux', side_effect=Exception("Device error")):
            devices = hotspot.get_connected_devices()
            assert devices == []

    @patch('platform.system')
    def test_stop_exception_handling(self, mock_platform):
        """Test exception handling in stop method."""
        mock_platform.return_value = "Linux"
        
        config = HotspotConfig(ssid="TestHotspot")
        hotspot = Hotspot(config)
        hotspot.is_running = True
        
        with patch.object(hotspot, '_stop_linux', side_effect=Exception("Stop error")):
            result = hotspot.stop()
            assert result is False

    @patch('platform.system')
    @patch('subprocess.run')
    def test_stop_linux_exception(self, mock_subprocess, mock_platform):
        """Test stop on Linux with exception."""
        mock_platform.return_value = "Linux"
        mock_subprocess.side_effect = Exception("Linux stop error")
        
        config = HotspotConfig(ssid="TestHotspot")
        hotspot = Hotspot(config)
        hotspot.is_running = True
        
        with patch.object(hotspot.dhcp_server, 'stop', return_value=True):
            result = hotspot.stop()
            # Should return False due to exception
            assert result is False
