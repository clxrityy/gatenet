# cli/__main__.py

import argparse
import sys

from cli.discover import run_discover
from cli.scan import run_scan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gatenet",
        description="Observe and inspect local networks"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    # discover command
    discover_parser = subparsers.add_parser(
        "discover",
        help="Discover devices on the local network"
    )
    discover_parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    # scan command
    scan_parser = subparsers.add_parser(
        "scan",
        help="Scan a host or subnet for open ports"
    )
    scan_parser.add_argument(
        "target",
        help="IP address or CIDR range"
    )
    scan_parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )

    return parser


def main() -> None:
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
