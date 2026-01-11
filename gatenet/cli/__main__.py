"""Command-line interface entrypoint for gatenet.

This module defines the argparse-based CLI used to invoke gatenet's
network discovery and scanning capabilities. It is a thin wrapper
around library functionality and contains no networking logic itself.
"""

import sys

from .parser import build_parser

from .discover import run_discover
from .scan import run_scan


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
        run_discover(json_output=args.json, resolve_names=args.resolve)
    elif args.command == "scan":
        run_scan(target=args.target, ports=args.ports, json_output=args.json)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
