"""
Gatenet CLI package entry point.

Usage:
    python -m gatenet.cli <command> [options]
    gatenet <command> [options] (if installed as a script)
"""


import argparse
from .commands import iface, wifi, trace, ping, dns, ports

OUTPUT_FORMAT_HELP = "Output format"

# Command handler registry
COMMANDS = {
    "iface": iface.cmd_iface,
    "wifi": wifi.cmd_wifi,
    "trace": trace.cmd_trace,
    "ping": ping.cmd_ping,
    "dns": dns.cmd_dns,
    "ports": ports.cmd_ports,
}


def main():
    parser = argparse.ArgumentParser(
        prog="gatenet",
        description="Gatenet CLI — networking diagnostics, discovery, and tools"
    )
    subparsers = parser.add_subparsers(dest="command")
    
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
    ports_parser.add_argument("--ports", nargs="*", type=int, default=None, help="Ports to scan (default: common)")
    ports_parser.add_argument("--output", choices=["json", "table", "plain"], default="table", help=OUTPUT_FORMAT_HELP)

    import sys
    from rich.console import Console
    args = parser.parse_args()
    handler = COMMANDS.get(args.command)
    if handler:
        handler(args)
    else:
        console = Console()
        console.print("[bold yellow]No command provided. Please choose one of the available commands below:[/bold yellow]\n")
        console.print(parser.format_help())
        sys.exit(2)
