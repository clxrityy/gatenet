"""
Integration tests for the hotspot module.
"""
import pytest
from unittest.mock import patch, MagicMock, mock_open
from gatenet.hotspot import Hotspot, HotspotConfig, SecurityType


class TestHotspotIntegration:
    """Integration tests for the complete hotspot functionality."""
    
    def _mock_subprocess_success(self, *args, **kwargs):
        """Mock subprocess calls to return success without prompting for passwords."""
        return MagicMock(returncode=0, stdout="", stderr="")
    
    def _mock_subprocess_failure(self, *args, **kwargs):
        """Mock subprocess calls to return failure."""
        return MagicMock(returncode=1, stdout="", stderr="Command failed")
    
    @patch('platform.system')
    @patch('subprocess.run')
    @patch('builtins.open', new_callable=mock_open)
    def test_create_secured_hotspot_linux(self, mock_file, mock_subprocess, mock_platform):
        """Test creating a complete secured hotspot on Linux."""
        mock_platform.return_value = "Linux"
        mock_subprocess.side_effect = self._mock_subprocess_success
        
        # Create hotspot configuration
        config = HotspotConfig(
            ssid="TestNetwork",
            password="SecurePass123!",
            interface="wlan0",
            channel=6,
            hidden=False
        )
        
        # Create hotspot instance
        hotspot = Hotspot(config)
        
        # Verify configuration
        assert hotspot.config.ssid == "TestNetwork"
        assert hotspot.config.password == "SecurePass123!"
        assert hotspot.security is not None
        assert hotspot.security.security_type == SecurityType.WPA2
        assert hotspot.dhcp_server is not None
        
        # Start the hotspot
        result = hotspot.start()
        assert result is True
        assert hotspot.is_running is True
        
        # Verify security configuration
        assert hotspot.security.validate_password() is True
        hostapd_config = hotspot.security.get_hostapd_config()
        assert "wpa=2" in hostapd_config
        assert "wpa_passphrase=SecurePass123!" in hostapd_config
        
        # Stop the hotspot
        result = hotspot.stop()
        assert result is True
        assert hotspot.is_running is False
    
    @patch('platform.system')
    def test_create_open_hotspot_macos(self, mock_platform):
        """Test creating an open hotspot on macOS."""
        mock_platform.return_value = "Darwin"
        
        # Create open hotspot configuration
        config = HotspotConfig(
            ssid="OpenNetwork",
            password=None,  # Open network
            interface="en0"
        )
        
        # Create hotspot instance
        hotspot = Hotspot(config)
        
        # Verify configuration
        assert hotspot.config.ssid == "OpenNetwork"
        assert hotspot.config.password is None
        assert hotspot.security is None  # No security for open network
        assert hotspot.dhcp_server is not None
        
        # Start the hotspot
        result = hotspot.start()
        assert result is True
        assert hotspot.is_running is True
    
    def test_password_generation_and_validation(self):
        """Test password generation and validation integration."""
        from gatenet.hotspot.security import SecurityConfig
        
        # Generate a strong password
        password = SecurityConfig.generate_password(16, include_symbols=True)
        assert len(password) == 16
        
        # Create security config with generated password
        config = SecurityConfig(password, SecurityType.WPA3)
        assert config.validate_password() is True
        
        # Verify it creates proper configuration
        hostapd_config = config.get_hostapd_config()
        assert "wpa=2" in hostapd_config
        assert f"wpa_passphrase={password}" in hostapd_config
        assert "SAE" in hostapd_config  # WPA3 uses SAE
        
        # Check security level
        assert config.get_security_level() == "Very High (WPA3)"
    
    @patch('platform.system')
    @patch('subprocess.run')
    def test_dhcp_configuration_integration(self, mock_subprocess, mock_platform):
        """Test DHCP server configuration integration."""
        mock_platform.return_value = "Linux"
        mock_subprocess.side_effect = self._mock_subprocess_success
        
        # Create hotspot with custom DHCP settings
        config = HotspotConfig(
            ssid="DHCPTest",
            password="TestPass123",
            ip_range="10.0.0.0/24",
            gateway="10.0.0.1"
        )
        
        hotspot = Hotspot(config)
        
        # Verify DHCP configuration
        assert hotspot.dhcp_server.ip_range == "10.0.0.0/24"
        assert hotspot.dhcp_server.gateway == "10.0.0.1"
        assert hotspot.dhcp_server.dns_servers == ["8.8.8.8", "8.8.4.4"]
        
        # Start DHCP server
        result = hotspot.dhcp_server.start()
        assert result is True
        assert hotspot.dhcp_server.is_running is True
    
    def test_error_handling_integration(self):
        """Test error handling across the hotspot system."""
        # Test invalid password
        config = HotspotConfig(ssid="Test", password="weak")
        hotspot = Hotspot(config)
        
        # Password should be invalid
        assert hotspot.security is not None
        assert hotspot.security.validate_password() is False
        
        # Test unsupported platform
        with patch('platform.system', return_value="Windows"):
            config = HotspotConfig(ssid="Test", password="StrongPass123!")
            hotspot = Hotspot(config)
            result = hotspot.start()
            assert result is False
    
    def test_configuration_chain(self):
        """Test the complete configuration chain."""
        # Start with basic config
        config = HotspotConfig(ssid="ChainTest", password="ChainTestPass123!")
        
        # Create hotspot
        hotspot = Hotspot(config)
        
        # Verify the chain
        assert config.ssid == "ChainTest"
        assert config.password == "ChainTestPass123!"
        assert hotspot.security is not None
        assert hotspot.security.password == "ChainTestPass123!"
        assert hotspot.security.security_type.value == "wpa2"  # Default security type
        assert hotspot.security.validate_password() is True
        
        # Verify DHCP uses default settings
        assert hotspot.dhcp_server.ip_range == "192.168.4.0/24"
        assert hotspot.dhcp_server.gateway == "192.168.4.1"
    
    @patch('platform.system')
    @patch('subprocess.run')
    @patch('builtins.open', new_callable=mock_open)
    def test_subprocess_mocking_prevents_prompts(self, mock_file, mock_subprocess, mock_platform):
        """Test that subprocess mocking prevents interactive password prompts."""
        mock_platform.return_value = "Linux"
        mock_subprocess.side_effect = self._mock_subprocess_success
        
        # Create a hotspot that would normally require sudo
        config = HotspotConfig(ssid="MockTest", password="TestPass123!")
        hotspot = Hotspot(config)
        
        # Start should work without prompting for password
        result = hotspot.start()
        assert result is True
        
        # Verify subprocess was called but didn't prompt
        assert mock_subprocess.called
        
        # Stop should also work without prompting
        result = hotspot.stop()
        assert result is True
    
    @patch('platform.system')
    @patch('subprocess.run')
    def test_subprocess_failure_handling(self, mock_subprocess, mock_platform):
        """Test handling of subprocess failures without prompts."""
        mock_platform.return_value = "Linux"
        mock_subprocess.side_effect = self._mock_subprocess_failure
        
        config = HotspotConfig(ssid="FailTest", password="TestPass123!")
        hotspot = Hotspot(config)
        
        # Should handle failure gracefully
        result = hotspot.start()
        assert result is False
        assert hotspot.is_running is False
