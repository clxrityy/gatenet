"""
trace.py — Implements the 'trace' CLI command for traceroute.
"""
def print_trace_json(hops, color, console):
    import json
    if color:
        console.print_json(json.dumps(hops))
    else:
        print(json.dumps(hops, indent=2))

def print_trace_plain(hops):
    for hop in hops:
        hopnum = hop.get("hop", "?")
        ip = hop.get("ip", "*")
        host = hop.get("hostname", "")
        rtt = hop.get("rtt_ms", None)
        rtt_str = f"{rtt:.2f} ms" if rtt is not None else "*"
        print(f"{hopnum}\t{ip}\t{host}\t{rtt_str}")

def print_trace_table(hops, color, console, host):
    from rich.table import Table
    table = Table(title=f"Traceroute to {host}", show_lines=True)
    table.add_column("Hop", style="cyan" if color else None)
    table.add_column("IP Address", style="green" if color else None)
    table.add_column("Hostname", style="magenta" if color else None)
    table.add_column("RTT", style="yellow" if color else None)
    for hop in hops:
        hopnum = str(hop.get("hop", "?"))
        ip = hop.get("ip", "*")
        hostname = hop.get("hostname", "")
        rtt = hop.get("rtt_ms", None)
        rtt_str = f"{rtt:.2f} ms" if rtt is not None else "*"
        table.add_row(hopnum, ip, hostname, rtt_str)
    console.print(table)

def cmd_trace(args):
    """
    Traceroute connectivity test CLI command.

    Runs a traceroute to the specified host and displays hop information in the selected output format.

    Args:
        args (argparse.Namespace):
            host (str): Host to traceroute.
            output_format (str, optional): Output style. One of 'table', 'plain', or 'json'.
            color (bool, optional): Enable colorized output. Default is True.
            verbosity (str or int, optional): Verbosity level. One of 'debug', 'info', 0, or 1. Default is 'info'.
            max_hops (int, optional): Maximum hops to trace.

    Example:
        .. code-block:: bash

           gatenet trace google.com --output plain --color false --max-hops 20

    Returns:
        None
    """
    from gatenet.diagnostics.traceroute import traceroute
    from rich.console import Console
    color = getattr(args, "color", True)
    output_format = getattr(args, "output_format", getattr(args, "output", "table"))
    console = Console()
    msg = f"[bold blue][trace] Running traceroute to {args.host}...[/bold blue]" if color else f"[trace] Running traceroute to {args.host}..."
    print_func = console.print if color else print
    print_func(msg)
    try:
        hops = traceroute(args.host, print_output=False)
        if not hops:
            console.print("[bold red]No hops found or traceroute failed.[/bold red]")
            raise SystemExit(1)
        if output_format == "json":
            print_trace_json(hops, color, console)
        elif output_format == "plain":
            print_trace_plain(hops)
        else:
            if color:
                print_trace_table(hops, color, console, args.host)
            else:
                print_trace_plain(hops)
    except Exception as e:
        console.print(f"[bold red][trace] Error: {e}[/bold red]")
        raise SystemExit(1)
