"""
Test the DHCP server functionality.
"""
import pytest
from unittest.mock import patch, MagicMock, mock_open
from gatenet.hotspot.dhcp import DHCPServer


class TestDHCPServer:
    """Test DHCP server functionality."""
    
    def _mock_subprocess_success(self, *args, **kwargs):
        """Mock subprocess calls to return success without prompting for passwords."""
        return MagicMock(returncode=0, stdout="", stderr="")
    
    def test_dhcp_server_creation_defaults(self):
        dhcp = DHCPServer("192.168.4.0/24", "192.168.4.1")
        assert dhcp.ip_range == "192.168.4.0/24"
        assert dhcp.gateway == "192.168.4.1"
        assert dhcp.dns_servers == ["8.8.8.8", "8.8.4.4"]
        assert dhcp.is_running is False
    
    def test_dhcp_server_creation_custom(self):
        dhcp = DHCPServer(
            ip_range="10.0.0.0/24",
            gateway="10.0.0.1",
            dns_servers=["1.1.1.1", "1.0.0.1"]
        )
        assert dhcp.ip_range == "10.0.0.0/24"
        assert dhcp.gateway == "10.0.0.1"
        assert dhcp.dns_servers == ["1.1.1.1", "1.0.0.1"]
    
    @patch('platform.system')
    @patch('subprocess.run')
    @patch('builtins.open', new_callable=mock_open)
    def test_start_linux_success(self, mock_file, mock_subprocess, mock_platform):
        mock_platform.return_value = "Linux"
        mock_subprocess.side_effect = self._mock_subprocess_success
        
        dhcp = DHCPServer("192.168.4.0/24", "192.168.4.1")
        result = dhcp.start()
        
        assert result is True
        assert dhcp.is_running is True
        mock_file.assert_called()
        mock_subprocess.assert_called()
    
    @patch('platform.system')
    @patch('subprocess.run')
    @patch('builtins.open', new_callable=mock_open)
    def test_start_linux_failure(self, mock_file, mock_subprocess, mock_platform):
        mock_platform.return_value = "Linux"
        mock_subprocess.return_value = MagicMock(returncode=1, stdout="", stderr="Command failed")
        
        dhcp = DHCPServer("192.168.4.0/24", "192.168.4.1")
        result = dhcp.start()
        
        assert result is False
        assert dhcp.is_running is False
    
    @patch('platform.system')
    def test_start_macos(self, mock_platform):
        mock_platform.return_value = "Darwin"
        
        dhcp = DHCPServer("192.168.4.0/24", "192.168.4.1")
        result = dhcp.start()
        
        assert result is True
        assert dhcp.is_running is True
    
    @patch('platform.system')
    def test_start_unsupported_platform(self, mock_platform):
        mock_platform.return_value = "Windows"
        
        dhcp = DHCPServer("192.168.4.0/24", "192.168.4.1")
        result = dhcp.start()
        
        assert result is False
        assert dhcp.is_running is False
    
    @patch('platform.system')
    @patch('subprocess.run')
    def test_stop_linux_success(self, mock_subprocess, mock_platform):
        mock_platform.return_value = "Linux"
        mock_subprocess.side_effect = self._mock_subprocess_success
        
        dhcp = DHCPServer("192.168.4.0/24", "192.168.4.1")
        dhcp.is_running = True
        
        result = dhcp.stop()
        
        assert result is True
        assert dhcp.is_running is False
    
    @patch('platform.system')
    @patch('subprocess.run')
    def test_stop_linux_failure(self, mock_subprocess, mock_platform):
        mock_platform.return_value = "Linux"
        mock_subprocess.side_effect = Exception("Command failed")
        
        dhcp = DHCPServer("192.168.4.0/24", "192.168.4.1")
        dhcp.is_running = True
        
        result = dhcp.stop()
        
        assert result is False
    
    @patch('platform.system')
    def test_stop_macos(self, mock_platform):
        mock_platform.return_value = "Darwin"
        
        dhcp = DHCPServer("192.168.4.0/24", "192.168.4.1")
        dhcp.is_running = True
        
        result = dhcp.stop()
        
        assert result is True
        assert dhcp.is_running is False
    
    def test_stop_not_running(self):
        dhcp = DHCPServer("192.168.4.0/24", "192.168.4.1")
        result = dhcp.stop()
        
        assert result is True
        assert dhcp.is_running is False
    
    @patch('platform.system')
    @patch('subprocess.run')
    def test_start_with_exception(self, mock_subprocess, mock_platform):
        mock_platform.return_value = "Linux"
        mock_subprocess.side_effect = Exception("Network error")
        
        dhcp = DHCPServer("192.168.4.0/24", "192.168.4.1")
        result = dhcp.start()
        
        assert result is False
        assert dhcp.is_running is False
