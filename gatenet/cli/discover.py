# cli/discover.py

from gatenet.discovery.aggregate import discover_devices
from .format import print_output


def run_discover(json_output: bool = False) -> None:
    """
    CLI handler for `gatenet discover`
    """
    devices = discover_devices()
    print_output(devices, json_output=json_output)
