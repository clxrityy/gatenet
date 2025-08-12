"""
Gatenet CLI package entry point.

Usage:
    python -m gatenet.cli <command> [options]
    gatenet <command> [options] (if installed as a script)
"""

import argparse
import sys

OUTPUT_FORMAT_HELP = "Output format"


def _load_handler(name):
    """Lazy import command handlers to avoid import-time optional deps."""
    if name == "iface":
        from .commands.iface import cmd_iface
        return cmd_iface
    if name == "wifi":
        from .commands.wifi import cmd_wifi
        return cmd_wifi
    if name == "trace":
        from .commands.trace import cmd_trace
        return cmd_trace
    if name == "ping":
        from .commands.ping import cmd_ping
        return cmd_ping
    if name == "dns":
        from .commands.dns import cmd_dns
        return cmd_dns
    if name == "ports":
        from .commands.ports import cmd_ports
        return cmd_ports
    if name == "hotspot":
        from .commands.hotspot import cmd_hotspot
        return cmd_hotspot
    return None


def main() -> int:
    """
    Entry point for the gatenet CLI.

    Examples:
        $ python -m gatenet.cli ping 8.8.8.8 --output json
        $ gatenet trace google.com --output table
    """
    from gatenet import __version__

    parser = argparse.ArgumentParser(
        prog="gatenet",
        description="Gatenet CLI — networking diagnostics, discovery, and tools",
    )
    subparsers = parser.add_subparsers(dest="command")

    # Subcommands
    iface_parser = subparsers.add_parser("iface", help="Network interface diagnostics")
    iface_parser.add_argument("--output", choices=["json", "table", "plain"], default="table", help=OUTPUT_FORMAT_HELP)

    wifi_parser = subparsers.add_parser("wifi", help="Scan and map Wi-Fi SSIDs")
    wifi_parser.add_argument("--output", choices=["json", "table", "plain"], default="table", help=OUTPUT_FORMAT_HELP)

    trace_parser = subparsers.add_parser("trace", help="Run traceroute connectivity test")
    trace_parser.add_argument("host", help="Target host for traceroute")
    trace_parser.add_argument("--output", choices=["json", "table", "plain"], default="table", help=OUTPUT_FORMAT_HELP)

    ping_parser = subparsers.add_parser("ping", help="Ping a host for connectivity test")
    ping_parser.add_argument("host", help="Target host to ping")
    ping_parser.add_argument("--output", choices=["json", "table", "plain"], default="table", help=OUTPUT_FORMAT_HELP)

    dns_parser = subparsers.add_parser("dns", help="DNS lookup and reverse lookup tools")
    dns_parser.add_argument("query", help="Domain or IP to resolve")
    dns_parser.add_argument("--output", choices=["json", "table", "plain"], default="table", help=OUTPUT_FORMAT_HELP)

    ports_parser = subparsers.add_parser("ports", help="Scan ports on a host")
    ports_parser.add_argument("host", help="Target host for port scan")
    ports_parser.add_argument(
        "--ports",
        nargs="*",
        type=int,
        default=None,
        help="Ports to scan (default: common ports: 21,22,23,25,53,80,110,143,443,3306,8080,8443,9000,27017)"
    )
    ports_parser.add_argument("--output", choices=["json", "table", "plain"], default="table", help=OUTPUT_FORMAT_HELP)

    hotspot_parser = subparsers.add_parser("hotspot", help="Create and manage Wi-Fi hotspots")
    hotspot_parser.add_argument("action", choices=["start", "stop", "status", "devices", "generate-password"], help="Action to perform")
    hotspot_parser.add_argument("--ssid", help="SSID name for the hotspot")
    hotspot_parser.add_argument("--password", help="Password for the hotspot")
    hotspot_parser.add_argument("--interface", default="wlan0", help="Network interface to use (default: wlan0)")
    hotspot_parser.add_argument("--ip-range", default="192.168.4.0/24", help="IP range for DHCP (default: 192.168.4.0/24)")
    hotspot_parser.add_argument("--gateway", default="192.168.4.1", help="Gateway IP (default: 192.168.4.1)")
    hotspot_parser.add_argument("--channel", type=int, default=6, help="Wi-Fi channel (default: 6)")
    hotspot_parser.add_argument("--security", choices=["open", "wpa", "wpa2", "wpa3"], default="wpa2", help="Security type (default: wpa2)")
    hotspot_parser.add_argument("--hidden", action="store_true", help="Create hidden SSID")
    hotspot_parser.add_argument("--length", type=int, default=12, help="Password length for generate-password (default: 12)")
    hotspot_parser.add_argument("--output", choices=["json", "table", "plain"], default="table", help=OUTPUT_FORMAT_HELP)

    # version
    subparsers.add_parser("version", help="Show version")

    args = parser.parse_args()

    if args.command == "version":
        print(__version__)
        return 0

    handler = _load_handler(args.command)
    if handler is not None:
        handler(args)
        return 0

    # No or unknown command: show help and exit cleanly (no error output)
    try:
        from rich.console import Console
        console = Console()
        console.print("[bold yellow]No command provided. Please choose one of the available commands below:[/bold yellow]\n")
        console.print(parser.format_help())
    except Exception:
        print("No command provided. See usage below:\n")
        print(parser.format_help())
    sys.exit(0)
