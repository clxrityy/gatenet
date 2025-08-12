"""
ports.py — Implements the 'ports' CLI command for port scanning.
"""
def _print_ports_output(console, host, results, output):
    from rich.table import Table
    import json
    if output == "json":
        console.print_json(json.dumps(results))
    elif output == "plain":
        for port, is_open in results:
            status = "OPEN" if is_open else "closed"
            print(f"{port}\t{status}")
    else:
        table = Table(title=f"Port Scan Results for {host}", show_lines=True)
        table.add_column("Port", style="cyan")
        table.add_column("Status", style="green")
        for port, is_open in results:
            status = "[green]OPEN[/green]" if is_open else "[red]closed[/red]"
            table.add_row(str(port), status)
        console.print(table)

def cmd_ports(args):
    """
    Port scanning CLI command.

    Scans the specified ports on the target host and displays results in the selected output format.

    Args:
        args (argparse.Namespace):
            host (str): Host to scan.
            ports (list[int], optional): List of ports to scan. Default: [22, 80, 443].
            output_format (str, optional): Output style. One of 'table', 'plain', or 'json'.
            color (bool, optional): Enable colorized output. Default is True.
            verbosity (str or int, optional): Verbosity level. One of 'debug', 'info', 0, or 1. Default is 'info'.

    Example:
        .. code-block:: bash

           gatenet ports 127.0.0.1 --ports 22 80 443 --output plain --color false

    Returns:
        None
    """
    from gatenet.diagnostics.port_scan import scan_ports
    from gatenet.utils import COMMON_PORTS
    from rich.console import Console
    console = Console()
    output_format = getattr(args, "output_format", getattr(args, "output", "table"))
    host = args.host
    # Use provided ports, or fall back to COMMON_PORTS if none/empty provided
    provided = getattr(args, "ports", None)
    ports = provided if provided else COMMON_PORTS
    console.print(f"[bold blue][ports] Scanning ports on {host}...[/bold blue]")
    try:
        results = scan_ports(host, ports=ports)
        if not results:
            console.print("[bold red]No ports scanned or scan failed.[/bold red]")
            raise SystemExit(1)
        _print_ports_output(console, host, results, output_format)
    except Exception as e:
        console.print(f"[bold red][ports] Error: {e}[/bold red]")
        raise SystemExit(1)
