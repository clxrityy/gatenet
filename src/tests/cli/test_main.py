"""
Tests for CLI main module and entry point.
"""
import pytest
import sys
from unittest.mock import patch, MagicMock

from gatenet.cli.main import main, COMMANDS


class TestCLIMain:
    """Test the main CLI entry point and command routing."""

    def test_main_no_command_shows_help(self, capsys):
        """Test that calling main without command shows help."""
        with patch.object(sys, 'argv', ['gatenet']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 2
            captured = capsys.readouterr()
            assert "No command provided" in captured.out

    def test_invalid_command_shows_help(self, capsys):
        """Test that invalid command shows help message."""
        with patch.object(sys, 'argv', ['gatenet', 'invalid_command']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 2
            captured = capsys.readouterr()
            assert "invalid choice" in captured.err  # argparse error message goes to stderr

    def test_commands_registry_has_expected_commands(self):
        """Test that COMMANDS registry contains expected command handlers."""
        expected_commands = ['ping', 'dns', 'trace', 'ports', 'iface', 'wifi', 'hotspot']
        for cmd in expected_commands:
            assert cmd in COMMANDS
            assert callable(COMMANDS[cmd])

    def test_main_calls_ping_handler(self):
        """Test that main() calls ping handler for ping command."""
        with patch.dict('gatenet.cli.main.COMMANDS', {'ping': MagicMock()}) as mock_commands:
            with patch.object(sys, 'argv', ['gatenet', 'ping', 'localhost']):
                main()
            mock_commands['ping'].assert_called_once()

    def test_main_calls_dns_handler(self):
        """Test that main() calls DNS handler for dns command."""
        with patch.dict('gatenet.cli.main.COMMANDS', {'dns': MagicMock()}) as mock_commands:
            with patch.object(sys, 'argv', ['gatenet', 'dns', 'example.com']):
                main()
            mock_commands['dns'].assert_called_once()

    def test_main_calls_trace_handler(self):
        """Test that main() calls traceroute handler for trace command."""
        with patch.dict('gatenet.cli.main.COMMANDS', {'trace': MagicMock()}) as mock_commands:
            with patch.object(sys, 'argv', ['gatenet', 'trace', 'google.com']):
                main()
            mock_commands['trace'].assert_called_once()

    def test_main_calls_ports_handler(self):
        """Test that main() calls ports handler for ports command."""
        with patch.dict('gatenet.cli.main.COMMANDS', {'ports': MagicMock()}) as mock_commands:
            with patch.object(sys, 'argv', ['gatenet', 'ports', '127.0.0.1']):
                main()
            mock_commands['ports'].assert_called_once()

    def test_main_calls_iface_handler(self):
        """Test that main() calls interface handler for iface command."""
        with patch.dict('gatenet.cli.main.COMMANDS', {'iface': MagicMock()}) as mock_commands:
            with patch.object(sys, 'argv', ['gatenet', 'iface']):
                main()
            mock_commands['iface'].assert_called_once()

    def test_main_calls_wifi_handler(self):
        """Test that main() calls wifi handler for wifi command."""
        with patch.dict('gatenet.cli.main.COMMANDS', {'wifi': MagicMock()}) as mock_commands:
            with patch.object(sys, 'argv', ['gatenet', 'wifi']):
                main()
            mock_commands['wifi'].assert_called_once()

    def test_main_calls_hotspot_handler(self):
        """Test that main() calls hotspot handler for hotspot command."""
        with patch.dict('gatenet.cli.main.COMMANDS', {'hotspot': MagicMock()}) as mock_commands:
            with patch.object(sys, 'argv', ['gatenet', 'hotspot', 'status']):
                main()
            mock_commands['hotspot'].assert_called_once()

    def test_ping_with_output_argument(self):
        """Test ping command with output argument."""
        mock_ping = MagicMock()
        mock_ping.return_value = {'status': 'success'}
        
        with patch.dict('gatenet.cli.main.COMMANDS', {'ping': mock_ping}):
            with patch.object(sys, 'argv', ['gatenet', 'ping', 'google.com', '--output', 'json']):
                main()
        
        mock_ping.assert_called_once()
        args = mock_ping.call_args[0][0]  # Get the first positional argument (args namespace)
        assert args.host == 'google.com'
        assert args.output == 'json'

    def test_dns_with_output_argument(self):
        """Test DNS command with output format argument."""
        with patch('gatenet.cli.commands.dns.cmd_dns') as mock_dns:
            mock_dns.return_value = {'status': 'success', 'ip': '1.2.3.4'}
            
            with patch.dict('gatenet.cli.main.COMMANDS', {'dns': mock_dns}):
                with patch.object(sys, 'argv', ['gatenet', 'dns', 'example.com', '--output', 'table']):
                    main()
            
            mock_dns.assert_called_once()
            args = mock_dns.call_args[0][0]
            assert args.query == 'example.com'
            assert args.output == 'table'

    def test_ports_with_custom_ports(self):
        """Test ports command with custom port list."""
        with patch('gatenet.cli.commands.ports.cmd_ports') as mock_ports:
            mock_ports.return_value = {'status': 'success', 'open_ports': [80, 443]}
            
            with patch.dict('gatenet.cli.main.COMMANDS', {'ports': mock_ports}):
                with patch.object(sys, 'argv', ['gatenet', 'ports', '127.0.0.1', '--ports', '80', '443', '22']):
                    main()
            
            mock_ports.assert_called_once()
            args = mock_ports.call_args[0][0]
            assert args.host == '127.0.0.1'
            assert args.ports == [80, 443, 22]


class TestMainModuleExecution:
    """Test direct module execution behavior."""

    def test_main_module_execution(self):
        """Test that module can be executed directly with proper mocking."""
        # Test the actual __main__.py module execution path
        # Simply test that the __main__ module exists and imports main
        from gatenet.cli.__main__ import main as main_from_main
        assert callable(main_from_main)
        assert main_from_main == main  # Should be the same function

    def test_main_function_import(self):
        """Test that main function can be imported and called."""
        # This test ensures the main function is properly exposed
        from gatenet.cli.main import main
        assert callable(main)
        
        # Test with help flag to avoid exit code 2
        with patch.object(sys, 'argv', ['gatenet', '--help']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            # Help exits with code 0
            assert exc_info.value.code == 0
