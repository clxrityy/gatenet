"""Argument parser for the gatenet CLI."""

import argparse


def _parse_ports(value: str) -> list[int]:
    """Parse a comma-separated string of ports into a list of integers.

    Args:
        value: Comma-separated string of port numbers.

    Returns:
        List of port numbers as integers.

    ```py
    ports = _parse_ports("22,80,443")
    ```
    """
    parts = [p.strip() for p in value.split(",") if p.strip()]

    try:
        ports = [int(p) for p in parts]
    except ValueError as e:
        raise argparse.ArgumentTypeError(
            f"""Invalid --ports value {value!r}.
            Expected comma-separated integers like 22,80,443."""
        ) from e
    for p in ports:
        if p < 1 or p > 65535:
            raise argparse.ArgumentTypeError(
                f"Port number {p} out of range. Must be between 1 and 65535."
            )
    return ports


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
    discover_parser.add_argument(
        "--resolve",
        action="store_true",
        help="Resolve hostnames via reverse DNS",
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
        "--ports",
        type=_parse_ports,
        default=[22, 80, 443],
        help="Comma-separated list of TCP ports to scan (default: 22,80,443)",
    )
    scan_parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )

    return parser
