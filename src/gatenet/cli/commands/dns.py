"""
dns.py — Implements the 'dns' CLI command for DNS lookups.
"""
def _build_dns_results(query, dns_lookup, reverse_dns_lookup):
    ip = dns_lookup(query)
    if ip != "Unknown" and ip != "Invalid Hostname":
        rev = reverse_dns_lookup(ip)
        return {"query": query, "ip": ip, "reverse": rev}
    else:
        rev = reverse_dns_lookup(query)
        if rev != "Unknown" and rev != "Invalid IP":
            return {"query": query, "reverse": rev}
        else:
            return {"query": query, "error": "Could not resolve as hostname or IP."}

def _print_dns_resolving(console, query, color, verbosity):
    """Prints the resolving message based on color and verbosity."""
    if verbosity > 0:
        msg = f"[dns] Resolving {query}..."
        if color:
            console.print(f"[bold blue]{msg}[/bold blue]")
        else:
            print(msg)

import json
from rich.table import Table

def _output_json(console, results, color):
    """Outputs DNS results in JSON format."""
    if color:
        console.print_json(json.dumps(results))
    else:
        print(json.dumps(results, indent=2))

def _output_plain(results):
    """Outputs DNS results in plain text format."""
    if "error" in results:
        print(f"error: {results['error']}", flush=True)
    else:
        print(f"{results.get('query','')} -> {results.get('ip','')} -> {results.get('reverse','')}", flush=True)

def _output_table(console, results, query, color):
    """Outputs DNS results in table format."""
    table = Table(title=f"DNS Results for {query}", show_lines=True)
    table.add_column("Field", style="cyan" if color else None)
    table.add_column("Value", style="green" if color else None)
    for k, v in results.items():
        table.add_row(str(k), str(v))
    if color:
        console.print(table)
    else:
        for k, v in results.items():
            print(f"{k}: {v}")

def _output_dns_results(console, results, query, output_format, color):
    """Handles output formatting for DNS results."""
    if output_format == "json":
        _output_json(console, results, color)
        return
    if output_format == "plain":
        _output_plain(results)
        return
    _output_table(console, results, query, color)

def cmd_dns(args):
    """
    DNS lookup and reverse lookup CLI command.

    Displays DNS resolution results for a domain or IP in the selected output format.

    Args:
        args (argparse.Namespace):
            query (str): Domain or IP to resolve.
            output_format (str, optional): Output style. One of 'table', 'plain', or 'json'.
            color (bool, optional): Enable colorized output. Default is True.
            verbosity (str or int, optional): Verbosity level. One of 'debug', 'info', 0, or 1. Default is 1.
            server (str, optional): Custom DNS server to use.

    Example:
        .. code-block:: bash

           gatenet dns google.com --output json --color false --server 1.1.1.1

    Returns:
        None
    """
    from gatenet.diagnostics.dns import dns_lookup, reverse_dns_lookup
    from rich.console import Console
    import sys

    console = Console()
    query = args.query
    output_format = getattr(args, "output_format", getattr(args, "output", "table"))
    color = getattr(args, "color", True)
    verbosity = getattr(args, "verbosity", 1)

    _print_dns_resolving(console, query, color, verbosity)

    try:
        results = _build_dns_results(query, dns_lookup, reverse_dns_lookup)
        _output_dns_results(console, results, query, output_format, color)
    except Exception as e:
        err_msg = f"[dns] Error: {e}"
        if color:
            console.print(f"[bold red]{err_msg}[/bold red]")
        else:
            print(err_msg)
        raise SystemExit(1)
