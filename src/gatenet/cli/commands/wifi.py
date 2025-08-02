"""
wifi.py — Implements the 'wifi' CLI command for Wi-Fi SSID scanning.
"""
def cmd_wifi(args):
    """
    Wi-Fi SSID scanning CLI command.

    Scans for available Wi-Fi networks and displays SSID, signal, and security in the selected output format.

    Args:
        args (argparse.Namespace):
            output_format (str, optional): Output style. One of 'table', 'plain', or 'json'.
            color (bool, optional): Enable colorized output. Default is True.
            verbosity (str or int, optional): Verbosity level. One of 'debug', 'info', 0, or 1. Default is 'info'.
            interface (str, optional): WiFi interface to scan.

    Example:
        .. code-block:: bash

           gatenet wifi --output plain --color false --interface en0

    Returns:
        None
    """
    output_format = getattr(args, 'output_format', getattr(args, 'output', 'table'))
    interface = getattr(args, 'interface', None)
    """
    Wi-Fi SSID scanning CLI command.

    Args:
        args: argparse.Namespace with 'output' attribute.

    Scans for available Wi-Fi networks and displays SSID, signal, and security in the selected output format.
    """
    from gatenet.utils import scan_wifi_networks
    from rich.console import Console
    from rich.table import Table
    import json
    console = Console()
    console.print("[bold blue][wifi] Scanning for Wi-Fi SSIDs...[/bold blue]")
    networks = scan_wifi_networks(interface)
    if not networks:
        console.print("[bold red]No Wi-Fi networks found.[/bold red]")
        raise SystemExit(1)
    if "error" in networks[0]:
        console.print(f"[bold red][wifi] Error: {networks[0]['error']}[/bold red]")
        raise SystemExit(1)
    if output_format == "json":
        console.print_json(json.dumps(networks))
    elif output_format == "plain":
        for net in networks:
            ssid = net.get("ssid", "")
            signal = net.get("signal", "")
            security = net.get("security", "")
            print(f"{ssid}\t{signal}\t{security}")
    else:
        table = Table(title="Wi-Fi Networks", show_lines=True)
        table.add_column("SSID", style="cyan")
        table.add_column("Signal", style="green")
        table.add_column("Security", style="magenta")
        for net in networks:
            table.add_row(
                net.get("ssid", ""),
                net.get("signal", ""),
                net.get("security", "")
            )
        console.print(table)
