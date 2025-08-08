"""
hotspot.py — Implements the 'hotspot' CLI command for Wi-Fi hotspot management.
"""
import json
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from gatenet.hotspot import Hotspot, HotspotConfig, SecurityConfig, SecurityType


def cmd_hotspot(args):
    """
    Wi-Fi hotspot management CLI command.

    Provides functionality to create, start, stop, and manage Wi-Fi access points.
    Supports various security configurations and device monitoring.

    Args:
        args (argparse.Namespace):
            action (str): Action to perform ('start', 'stop', 'status', 'devices', 'generate-password')
            ssid (str, optional): SSID name for the hotspot
            password (str, optional): Password for the hotspot (if secured)
            interface (str, optional): Network interface to use (default: wlan0)
            ip_range (str, optional): IP range for DHCP (default: 192.168.4.0/24)
            gateway (str, optional): Gateway IP (default: 192.168.4.1)
            channel (int, optional): Wi-Fi channel (default: 6)
            security (str, optional): Security type (open, wpa, wpa2, wpa3)
            hidden (bool, optional): Create hidden SSID
            output (str, optional): Output format (table, json, plain)

    Example:
        .. code-block:: bash

           gatenet hotspot start --ssid MyHotspot --password mypass123 --security wpa2
           gatenet hotspot status --output json
           gatenet hotspot devices --output table
           gatenet hotspot stop
           gatenet hotspot generate-password --length 16

    Returns:
        None
    """
    console = Console()
    output_format = getattr(args, 'output', 'table')
    
    try:
        if args.action == 'generate-password':
            _handle_generate_password(args, console, output_format)
        elif args.action == 'start':
            _handle_start_hotspot(args, console, output_format)
        elif args.action == 'stop':
            _handle_stop_hotspot(console, output_format)
        elif args.action == 'status':
            _handle_hotspot_status(console, output_format)
        elif args.action == 'devices':
            _handle_connected_devices(console, output_format)
        else:
            console.print(f"[red]Unknown action: {args.action}[/red]")
            sys.exit(1)
    except Exception as e:
        if output_format == 'json':
            result = {"error": str(e), "success": False}
            console.print(json.dumps(result, indent=2))
        else:
            console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


def _handle_generate_password(args, console, output_format):
    """Generate a secure password for hotspot use."""
    length = getattr(args, 'length', 12)
    password = SecurityConfig.generate_password(length)
    
    if output_format == 'json':
        result = {
            "password": password,
            "length": len(password),
            "strength": "strong",
            "success": True
        }
        console.print(json.dumps(result, indent=2))
    elif output_format == 'plain':
        console.print(password)
    else:
        panel = Panel(
            f"[green]{password}[/green]",
            title="Generated Password",
            subtitle=f"Length: {len(password)} characters",
            border_style="green"
        )
        console.print(panel)


def _handle_start_hotspot(args, console, output_format):
    """Start a Wi-Fi hotspot."""
    if not args.ssid:
        console.print("[red]Error: SSID is required to start hotspot[/red]")
        sys.exit(1)
    
    # Parse and validate security configuration
    security_type, password = _parse_security_config(args, console)
    
    # Create hotspot configuration
    config = _create_hotspot_config(args, password, security_type)
    
    # Create and start hotspot
    hotspot = Hotspot(config)
    success = hotspot.start()
    
    # Output results
    _output_start_result(args, config, security_type, success, console, output_format)


def _parse_security_config(args, console):
    """Parse security configuration from arguments."""
    security_type = SecurityType.OPEN
    if hasattr(args, 'security') and args.security:
        try:
            security_type = SecurityType(args.security.lower())
        except ValueError:
            console.print(f"[red]Invalid security type: {args.security}[/red]")
            sys.exit(1)
    
    # Validate password if security is not open
    password = args.password
    if security_type != SecurityType.OPEN and not password:
        console.print("[red]Error: Password is required for secured networks[/red]")
        sys.exit(1)
    
    return security_type, password


def _create_hotspot_config(args, password, security_type):
    """Create hotspot configuration from arguments."""
    return HotspotConfig(
        ssid=args.ssid,
        password=password if security_type != SecurityType.OPEN else None,
        interface=getattr(args, 'interface', 'wlan0'),
        ip_range=getattr(args, 'ip_range', '192.168.4.0/24'),
        gateway=getattr(args, 'gateway', '192.168.4.1'),
        channel=getattr(args, 'channel', 6),
        hidden=getattr(args, 'hidden', False)
    )


def _output_start_result(args, config, security_type, success, console, output_format):
    """Output the start hotspot result."""
    if output_format == 'json':
        result = {
            "success": success,
            "ssid": args.ssid,
            "security": security_type.value,
            "interface": config.interface,
            "gateway": config.gateway,
            "message": "Hotspot started successfully" if success else "Failed to start hotspot"
        }
        console.print(json.dumps(result, indent=2))
    elif output_format == 'plain':
        message = f"Hotspot '{args.ssid}' started successfully" if success else f"Failed to start hotspot '{args.ssid}'"
        console.print(message)
    else:
        _output_start_table(args, config, security_type, success, console)


def _output_start_table(args, config, security_type, success, console):
    """Output start result as a table."""
    if success:
        table = Table(title="Hotspot Started", border_style="green")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("SSID", args.ssid)
        table.add_row("Security", security_type.value.upper())
        table.add_row("Interface", config.interface)
        table.add_row("Gateway", config.gateway)
        table.add_row("Channel", str(config.channel))
        table.add_row("Hidden", "Yes" if config.hidden else "No")
        
        console.print(table)
    else:
        console.print(f"[red]Failed to start hotspot '{args.ssid}'[/red]")


def _handle_stop_hotspot(console, output_format):
    """Stop the running hotspot."""
    # For stop, we need to create a minimal config just to instantiate Hotspot
    # In a real implementation, you might want to store the running config
    config = HotspotConfig(ssid="temp")
    hotspot = Hotspot(config)
    success = hotspot.stop()
    
    if output_format == 'json':
        result = {
            "success": success,
            "message": "Hotspot stopped successfully" if success else "Failed to stop hotspot or no hotspot running"
        }
        console.print(json.dumps(result, indent=2))
    elif output_format == 'plain':
        if success:
            console.print("Hotspot stopped successfully")
        else:
            console.print("Failed to stop hotspot or no hotspot running")
    else:
        if success:
            console.print("[green]Hotspot stopped successfully[/green]")
        else:
            console.print("[yellow]Failed to stop hotspot or no hotspot running[/yellow]")


def _handle_hotspot_status(console, output_format):
    """Check hotspot status."""
    # Create a minimal config for status checking
    config = HotspotConfig(ssid="temp")
    hotspot = Hotspot(config)
    
    if output_format == 'json':
        result = {
            "running": hotspot.is_running,
            "platform": hotspot.system,
            "success": True
        }
        console.print(json.dumps(result, indent=2))
    elif output_format == 'plain':
        status = "running" if hotspot.is_running else "stopped"
        console.print(f"Hotspot status: {status}")
    else:
        status_color = "green" if hotspot.is_running else "red"
        status_text = "Running" if hotspot.is_running else "Stopped"
        
        table = Table(title="Hotspot Status", border_style=status_color)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style=status_color)
        
        table.add_row("Status", status_text)
        table.add_row("Platform", hotspot.system)
        
        console.print(table)


def _handle_connected_devices(console, output_format):
    """List connected devices."""
    config = HotspotConfig(ssid="temp")
    hotspot = Hotspot(config)
    
    try:
        devices = hotspot.get_connected_devices()
    except Exception as e:
        _output_devices_error(e, console, output_format)
        return
    
    _output_devices_result(devices, console, output_format)


def _output_devices_error(error, console, output_format):
    """Output error for connected devices command."""
    if output_format == 'json':
        result = {"error": str(error), "success": False}
        console.print(json.dumps(result, indent=2))
    else:
        console.print(f"[red]Error getting connected devices: {error}[/red]")


def _output_devices_result(devices, console, output_format):
    """Output connected devices result."""
    if output_format == 'json':
        result = {
            "devices": devices,
            "count": len(devices),
            "success": True
        }
        console.print(json.dumps(result, indent=2))
    elif output_format == 'plain':
        _output_devices_plain(devices, console)
    else:
        _output_devices_table(devices, console)


def _output_devices_plain(devices, console):
    """Output devices in plain format."""
    if devices:
        for device in devices:
            console.print(f"{device.get('ip', 'N/A')} - {device.get('mac', 'N/A')} - {device.get('hostname', 'Unknown')}")
    else:
        console.print("No devices connected")


def _output_devices_table(devices, console):
    """Output devices in table format."""
    if devices:
        table = Table(title=f"Connected Devices ({len(devices)})", border_style="green")
        table.add_column("IP Address", style="cyan")
        table.add_column("MAC Address", style="yellow")
        table.add_column("Hostname", style="green")
        table.add_column("Connection Time", style="blue")
        
        for device in devices:
            table.add_row(
                device.get('ip', 'N/A'),
                device.get('mac', 'N/A'),
                device.get('hostname', 'Unknown'),
                device.get('connected_time', 'N/A')
            )
        
        console.print(table)
    else:
        console.print("[yellow]No devices currently connected[/yellow]")
