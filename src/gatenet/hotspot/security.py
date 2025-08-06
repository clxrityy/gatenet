"""
Security configuration for hotspot access points.
"""
import secrets
import string
from typing import Optional
from enum import Enum


class SecurityType(Enum):
    """Security types for Wi-Fi access points."""
    OPEN = "open"
    WEP = "wep"
    WPA = "wpa"
    WPA2 = "wpa2"
    WPA3 = "wpa3"


class SecurityConfig:
    """
    Manage security settings for Wi-Fi hotspots.
    
    Example:
        >>> from gatenet.hotspot import SecurityConfig, SecurityType
        >>> config = SecurityConfig("mypassword123", SecurityType.WPA2)
        >>> config.validate_password()
        >>> strong_password = SecurityConfig.generate_password()
    """
    
    def __init__(self, password: Optional[str] = None, 
                 security_type: SecurityType = SecurityType.WPA2):
        self.password = password
        self.security_type = security_type
        
    def validate_password(self) -> bool:
        """
        Validate the password strength.
        
        Returns:
            bool: True if password meets security requirements
            
        Example:
            >>> config = SecurityConfig("weakpass")
            >>> config.validate_password()  # False
            >>> config = SecurityConfig("StrongPass123!")
            >>> config.validate_password()  # True
        """
        if not self.password:
            return self.security_type == SecurityType.OPEN
        
        # WPA2/WPA3 password requirements
        if self.security_type in [SecurityType.WPA2, SecurityType.WPA3]:
            if len(self.password) < 8:
                return False
            if len(self.password) > 63:
                return False
            # Check for common weak patterns
            weak_patterns = ["password", "123456", "qwerty", "admin"]
            if any(pattern in self.password.lower() for pattern in weak_patterns):
                return False
            return True
        
        # WEP password requirements (legacy, not recommended)
        if self.security_type == SecurityType.WEP:
            return len(self.password) in [5, 13, 16, 29]
        
        return True
    
    def get_hostapd_config(self) -> str:
        """
        Generate hostapd configuration for the security settings.
        
        Returns:
            str: Configuration lines for hostapd
        """
        if self.security_type == SecurityType.OPEN:
            return ""
        
        if self.security_type == SecurityType.WPA2:
            return f"""wpa=2
wpa_passphrase={self.password}
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP"""
        
        if self.security_type == SecurityType.WPA3:
            return f"""wpa=2
wpa_passphrase={self.password}
wpa_key_mgmt=SAE
rsn_pairwise=CCMP"""
        
        if self.security_type == SecurityType.WEP:
            # WEP is deprecated and insecure
            return f"""wep_default_key=0
wep_key0="{self.password}" """
        
        return ""
    
    @staticmethod
    def generate_password(length: int = 12, include_symbols: bool = True) -> str:
        """
        Generate a strong random password.
        
        Args:
            length (int): Password length (minimum 8)
            include_symbols (bool): Include special characters
            
        Returns:
            str: Strong random password
            
        Example:
            >>> password = SecurityConfig.generate_password(16)
            >>> len(password) == 16  # True
        """
        if length < 8:
            length = 8
        
        # Build character set
        chars = string.ascii_letters + string.digits
        if include_symbols:
            chars += "!@#$%^&*"
        
        # Ensure at least one of each type
        password = [
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.digits)
        ]
        
        if include_symbols:
            password.append(secrets.choice("!@#$%^&*"))
        
        # Fill remaining length
        for _ in range(length - len(password)):
            password.append(secrets.choice(chars))
        
        # Shuffle the password
        secrets.SystemRandom().shuffle(password)
        
        return ''.join(password)
    
    def get_security_level(self) -> str:
        """
        Get a human-readable security level description.
        
        Returns:
            str: Security level description
        """
        if self.security_type == SecurityType.OPEN:
            return "None (Open network)"
        elif self.security_type == SecurityType.WEP:
            return "Low (WEP - deprecated)"
        elif self.security_type == SecurityType.WPA:
            return "Medium (WPA)"
        elif self.security_type == SecurityType.WPA2:
            return "High (WPA2)"
        elif self.security_type == SecurityType.WPA3:
            return "Very High (WPA3)"
        else:
            return "Unknown"
