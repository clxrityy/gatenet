"""CLI handler for network port scanning.

This module connects the gatenet port scanning functionality to the
command-line interface. It is responsible only for invoking the scan
and formatting the output for display.
"""

from typing import Iterable
from gatenet.scan.ports import scan_target
from .format import print_output


def run_scan(target: str, ports: Iterable[int], json_output: bool = False) -> None:
    """Execute the `gatenet scan` command.

    Runs a port scan against the specified target and prints the
    results to standard output in either human-readable or JSON format.

    Args:
        target: IP address, hostname, or CIDR range to scan.
        ports: Iterable of port numbers to scan.
        json_output: If True, output results as JSON.

    ```py
    from gatenet.cli.scan import run_scan
    run_scan("example.com", ports=[22, 80, 443], json_output=True)
    ```
    """
    result = scan_target(target, ports=ports)
    print_output(result, json_output=json_output)
