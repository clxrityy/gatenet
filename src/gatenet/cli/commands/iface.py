"""
iface.py — Implements the 'iface' CLI command for network interface scanning.
"""
def _print_no_interfaces(console, color: bool) -> None:
    if color:
        console.print("[bold red]No network interfaces found.[/bold red]")
    else:
        print("No network interfaces found.")

def _print_debug(console, color: bool, count: int) -> None:
    msg = f"[iface] Found {count} interfaces."
    if color:
        console.print(f"[bold blue]{msg}[/bold blue]")
    else:
        print(msg)

def _print_json(console, color: bool, interfaces) -> None:
    import json
    if color:
        console.print_json(json.dumps(interfaces))
    else:
        print(json.dumps(interfaces, indent=2))

def _print_plain(interfaces) -> None:
    for iface in interfaces:
        name = iface.get("name", "?")
        ip = iface.get("ip", "?")
        mac = iface.get("mac", "?")
        print(f"{name}\t{ip}\t{mac}")

def _print_table(console, color: bool, interfaces) -> None:
    from rich.table import Table
    table = Table(title="Network Interfaces", show_lines=True)
    table.add_column("Name", style="cyan" if color else None)
    table.add_column("IP Address", style="green" if color else None)
    table.add_column("MAC Address", style="magenta" if color else None)
    for iface in interfaces:
        table.add_row(
            iface.get("name", "?"),
            iface.get("ip", "?"),
            iface.get("mac", "?")
        )
    if color:
        console.print(table)
    else:
        _print_plain(interfaces)

def cmd_iface(args):
    """
    Network interface diagnostics CLI command.

    Lists all network interfaces with IP and MAC addresses in the selected output format.

    Args:
        args (argparse.Namespace):
            output_format (str, optional): Output style. One of 'table', 'plain', or 'json'.
            color (bool, optional): Enable colorized output. Default is True.
            verbosity (str or int, optional): Verbosity level. One of 'debug', 'info', 0, or 1. Default is 'info'.
            default (str, optional): Show this interface first if present.

    Example:
        .. code-block:: bash

           gatenet iface --output json --color false --verbosity debug --default eth0

    Returns:
        None
    """
    output_format = getattr(args, 'output_format', 'table')
    color = getattr(args, 'color', True)
    verbosity = getattr(args, 'verbosity', 'info')
    default_iface = getattr(args, 'default', None)
    from gatenet.utils import list_network_interfaces
    from rich.console import Console
    console = Console()
    interfaces = list_network_interfaces()
    if not interfaces:
        _print_no_interfaces(console, color)
        raise SystemExit(1)
    if default_iface:
        interfaces = sorted(interfaces, key=lambda x: x.get("name") != default_iface)
    if verbosity == "debug":
        _print_debug(console, color, len(interfaces))
    if output_format == "json":
        _print_json(console, color, interfaces)
    elif output_format == "plain":
        _print_plain(interfaces)
    else:
        _print_table(console, color, interfaces)
