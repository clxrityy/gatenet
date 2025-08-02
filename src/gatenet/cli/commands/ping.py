"""
ping.py — Implements the 'ping' CLI command for connectivity tests.
"""
def cmd_ping(args):
    """
    Ping connectivity test CLI command.

    Pings the specified host and displays latency statistics in the selected output format.

    Args:
        args (argparse.Namespace):
            host (str): Host to ping.
            output_format (str, optional): Output style. One of 'table', 'plain', or 'json'.
            color (bool, optional): Enable colorized output. Default is True.
            verbosity (str or int, optional): Verbosity level. One of 'debug', 'info', 0, or 1. Default is 'info'.
            count (int, optional): Number of pings to send.

    Example:
        .. code-block:: bash

           gatenet ping 8.8.8.8 --count 4 --output json --color false

    Returns:
        None
    """
    from gatenet.diagnostics.ping import ping
    from rich.console import Console
    from rich.table import Table
    import json
    console = Console()
    console.print(f"[bold blue][ping] Pinging {args.host}...[/bold blue]")
    try:
        result = ping(args.host)
        if not result.get("success"):
            console.print(f"[bold red][ping] Error: {result.get('error', 'Ping failed')}[/bold red]")
            raise SystemExit(1)
        output_format = getattr(args, "output_format", getattr(args, "output", "table"))
        def fmt(val):
            try:
                return f"{float(val):.2f}"
            except (ValueError, TypeError):
                return str(val) if val is not None else "?"
        if output_format == "json":
            console.print_json(json.dumps(result))
        elif output_format == "plain":
            print(f"min={fmt(result.get('rtt_min'))} avg={fmt(result.get('rtt_avg'))} max={fmt(result.get('rtt_max'))} jitter={fmt(result.get('jitter'))} loss={result.get('packet_loss', '?')}%", flush=True)
        else:
            table = Table(title=f"Ping Results for {args.host}", show_lines=True)
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            table.add_row("Min RTT", f"{fmt(result.get('rtt_min'))} ms")
            table.add_row("Avg RTT", f"{fmt(result.get('rtt_avg'))} ms")
            table.add_row("Max RTT", f"{fmt(result.get('rtt_max'))} ms")
            table.add_row("Jitter", f"{fmt(result.get('jitter'))} ms")
            table.add_row("Packet Loss", f"{result.get('packet_loss', '?')}%")
            console.print(table)
    except Exception as e:
        console.print(f"[bold red][ping] Error: {e}[/bold red]")
        raise SystemExit(1)
