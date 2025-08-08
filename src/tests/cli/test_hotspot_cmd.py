"""
Tests for CLI hotspot command.
"""
import pytest
import json
from unittest.mock import patch, MagicMock
from argparse import Namespace

from gatenet.cli.commands.hotspot import cmd_hotspot


class TestHotspotCommand:
    """Test the hotspot CLI command."""

    def test_generate_password_table_output(self, capsys):
        """Test password generation with table output."""
        args = Namespace(action='generate-password', length=12, output='table')
        
        with patch('gatenet.cli.commands.hotspot.SecurityConfig.generate_password') as mock_gen:
            mock_gen.return_value = 'test_password_123'
            cmd_hotspot(args)
            
        captured = capsys.readouterr()
        assert 'Generated Password' in captured.out
        assert 'test_password_123' in captured.out
        assert 'Length: 17 characters' in captured.out  # Length of 'test_password_123'

    def test_generate_password_json_output(self, capsys):
        """Test password generation with JSON output."""
        args = Namespace(action='generate-password', length=16, output='json')
        
        with patch('gatenet.cli.commands.hotspot.SecurityConfig.generate_password') as mock_gen:
            mock_gen.return_value = 'secure_password_16'
            cmd_hotspot(args)
            
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result['password'] == 'secure_password_16'
        assert result['length'] == 18  # Length of 'secure_password_16'
        assert result['strength'] == 'strong'
        assert result['success'] is True

    def test_generate_password_plain_output(self, capsys):
        """Test password generation with plain output."""
        args = Namespace(action='generate-password', length=8, output='plain')
        
        with patch('gatenet.cli.commands.hotspot.SecurityConfig.generate_password') as mock_gen:
            mock_gen.return_value = 'plain123'
            cmd_hotspot(args)
            
        captured = capsys.readouterr()
        assert captured.out.strip() == 'plain123'

    def test_start_hotspot_success(self, capsys):
        """Test starting hotspot successfully."""
        args = Namespace(
            action='start',
            ssid='TestHotspot',
            password='testpass123',
            security='wpa2',
            interface='wlan0',
            ip_range='192.168.4.0/24',
            gateway='192.168.4.1',
            channel=6,
            hidden=False,
            output='json'
        )
        
        with patch('gatenet.cli.commands.hotspot.Hotspot') as mock_hotspot_class:
            mock_hotspot = MagicMock()
            mock_hotspot.start.return_value = True
            mock_hotspot_class.return_value = mock_hotspot
            
            cmd_hotspot(args)
            
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result['success'] is True
        assert result['ssid'] == 'TestHotspot'
        assert result['security'] == 'wpa2'

    def test_start_hotspot_missing_ssid(self, capsys):
        """Test starting hotspot without SSID."""
        args = Namespace(action='start', ssid=None, output='table')
        
        with pytest.raises(SystemExit) as exc_info:
            cmd_hotspot(args)
        
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert 'SSID is required' in captured.out

    def test_start_hotspot_invalid_security(self, capsys):
        """Test starting hotspot with invalid security type."""
        args = Namespace(
            action='start',
            ssid='TestHotspot',
            password='testpass',
            security='invalid',
            output='table'
        )
        
        with pytest.raises(SystemExit) as exc_info:
            cmd_hotspot(args)
        
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert 'Invalid security type' in captured.out

    def test_start_hotspot_secured_without_password(self, capsys):
        """Test starting secured hotspot without password."""
        args = Namespace(
            action='start',
            ssid='TestHotspot',
            password=None,
            security='wpa2',
            output='table'
        )
        
        with pytest.raises(SystemExit) as exc_info:
            cmd_hotspot(args)
        
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert 'Password is required for secured networks' in captured.out

    def test_stop_hotspot_success(self, capsys):
        """Test stopping hotspot successfully."""
        args = Namespace(action='stop', output='json')
        
        with patch('gatenet.cli.commands.hotspot.Hotspot') as mock_hotspot_class:
            mock_hotspot = MagicMock()
            mock_hotspot.stop.return_value = True
            mock_hotspot_class.return_value = mock_hotspot
            
            cmd_hotspot(args)
            
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result['success'] is True
        assert 'stopped successfully' in result['message']

    def test_status_command(self, capsys):
        """Test hotspot status command."""
        args = Namespace(action='status', output='json')
        
        with patch('gatenet.cli.commands.hotspot.Hotspot') as mock_hotspot_class:
            mock_hotspot = MagicMock()
            mock_hotspot.is_running = False
            mock_hotspot.system = 'Linux'
            mock_hotspot_class.return_value = mock_hotspot
            
            cmd_hotspot(args)
            
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result['running'] is False
        assert result['platform'] == 'Linux'
        assert result['success'] is True

    def test_devices_command_success(self, capsys):
        """Test connected devices command with devices."""
        args = Namespace(action='devices', output='json')
        
        mock_devices = [
            {'ip': '192.168.4.10', 'mac': '00:11:22:33:44:55', 'hostname': 'device1'},
            {'ip': '192.168.4.11', 'mac': '00:11:22:33:44:56', 'hostname': 'device2'}
        ]
        
        with patch('gatenet.cli.commands.hotspot.Hotspot') as mock_hotspot_class:
            mock_hotspot = MagicMock()
            mock_hotspot.get_connected_devices.return_value = mock_devices
            mock_hotspot_class.return_value = mock_hotspot
            
            cmd_hotspot(args)
            
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result['devices'] == mock_devices
        assert result['count'] == 2
        assert result['success'] is True

    def test_devices_command_error(self, capsys):
        """Test connected devices command with error."""
        args = Namespace(action='devices', output='json')
        
        with patch('gatenet.cli.commands.hotspot.Hotspot') as mock_hotspot_class:
            mock_hotspot = MagicMock()
            mock_hotspot.get_connected_devices.side_effect = Exception('Network error')
            mock_hotspot_class.return_value = mock_hotspot
            
            cmd_hotspot(args)
            
        captured = capsys.readouterr()
        result = json.loads(captured.out)
        assert result['error'] == 'Network error'
        assert result['success'] is False

    def test_unknown_action(self, capsys):
        """Test unknown action handling."""
        args = Namespace(action='unknown', output='table')
        
        with pytest.raises(SystemExit) as exc_info:
            cmd_hotspot(args)
        
        assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert 'Unknown action: unknown' in captured.out

    def test_command_exception_handling(self, capsys):
        """Test general exception handling."""
        args = Namespace(action='generate-password', length=12, output='json')
        
        with patch('gatenet.cli.commands.hotspot.SecurityConfig.generate_password') as mock_gen:
            mock_gen.side_effect = Exception('Password generation failed')
            
            with pytest.raises(SystemExit) as exc_info:
                cmd_hotspot(args)
            
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            result = json.loads(captured.out)
            assert result['error'] == 'Password generation failed'
            assert result['success'] is False
