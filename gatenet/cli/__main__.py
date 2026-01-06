"""Command-line interface entrypoint for gatenet.

This module defines the argparse-based CLI used to invoke gatenet's
network discovery and scanning capabilities. It is a thin wrapper
around library functionality and contains no networking logic itself.
"""

import argparse
import sys

from .discover import run_discover
from .scan import run_scan


def build_parser() -> argparse.ArgumentParser:
    """Construct the argument parser for the gatenet CLI.

    This function defines all supported commands, subcommands, and
    flags exposed to end users.

    Returns:
        An initialized ArgumentParser instance.

    ```py
    parser = build_parser()
    ```
    """
    parser = argparse.ArgumentParser(
        prog="gatenet",
        description="Observe and inspect local networks",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # discover command
    discover_parser = subparsers.add_parser(
        "discover",
        help="Discover devices on the local network",
    )
    discover_parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )

    # scan command
    scan_parser = subparsers.add_parser(
        "scan",
        help="Scan a host or subnet for open ports",
    )
    scan_parser.add_argument(
        "target",
        help="IP address or CIDR range",
    )
    scan_parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )

    return parser


def main() -> None:
    """CLI entrypoint for gatenet.

    Parses command-line arguments and dispatches execution to the
    appropriate command handler.

    ```py
    if __name__ == "__main__":
        main()
    ```
    """
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "discover":
        run_discover(json_output=args.json)
    elif args.command == "scan":
        run_scan(target=args.target, json_output=args.json)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
