"""CLI handler for network device discovery.

This module connects the gatenet discovery library to the command-line
interface. It performs no discovery logic itself and is responsible
only for orchestration and output formatting.
"""

from gatenet.discovery.aggregate import discover_devices
from .format import print_output


def run_discover(json_output: bool = False) -> None:
    """Execute the `gatenet discover` command.

    Runs available device discovery mechanisms and prints the results
    to standard output in either human-readable or JSON format.

    Args:
        json_output: If True, output results as JSON.
    """
    devices = discover_devices()
    print_output(devices, json_output=json_output)
