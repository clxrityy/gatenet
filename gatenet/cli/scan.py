# cli/scan.py

from gatenet.scan.ports import scan_target
from .format import print_output


def run_scan(target: str, json_output: bool = False) -> None:
    """
    CLI handler for `gatenet scan`
    """
    result = scan_target(target)
    print_output(result, json_output=json_output)
