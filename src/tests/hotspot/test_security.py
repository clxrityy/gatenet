"""
Test the security configuration functionality.
"""
import pytest
from gatenet.hotspot.security import SecurityConfig, SecurityType


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
            (SecurityType.WPA, "Medium (WPA)"),
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
    
    def test_hostapd_config_wpa3(self):
        config = SecurityConfig("testpass", SecurityType.WPA3)
        hostapd_config = config.get_hostapd_config()
        assert "wpa=2" in hostapd_config
        assert "wpa_passphrase=testpass" in hostapd_config
        assert "SAE" in hostapd_config
    
    def test_hostapd_config_wep(self):
        config = SecurityConfig("testpass", SecurityType.WEP)
        hostapd_config = config.get_hostapd_config()
        assert "wep_default_key=0" in hostapd_config
        assert "wep_key0=" in hostapd_config
    
    def test_hostapd_config_open(self):
        config = SecurityConfig(None, SecurityType.OPEN)
        hostapd_config = config.get_hostapd_config()
        assert hostapd_config == ""
    
    def test_security_type_enum_values(self):
        assert SecurityType.OPEN.value == "open"
        assert SecurityType.WEP.value == "wep"
        assert SecurityType.WPA.value == "wpa"
        assert SecurityType.WPA2.value == "wpa2"
        assert SecurityType.WPA3.value == "wpa3"
    
    def test_wep_password_validation(self):
        # WEP accepts specific lengths: 5, 13, 16, 29
        config = SecurityConfig("hello", SecurityType.WEP)  # 5 chars
        assert config.validate_password() is True
        
        config = SecurityConfig("1234567890123", SecurityType.WEP)  # 13 chars
        assert config.validate_password() is True
        
        config = SecurityConfig("wronglength", SecurityType.WEP)  # wrong length
        assert config.validate_password() is False
    
    def test_password_none_for_secured_network(self):
        config = SecurityConfig(None, SecurityType.WPA2)
        assert config.validate_password() is False
    
    def test_password_too_long(self):
        # WPA2/WPA3 passwords cannot be longer than 63 characters
        long_password = "a" * 64
        config = SecurityConfig(long_password, SecurityType.WPA2)
        assert config.validate_password() is False
