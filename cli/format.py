# cli/format.py

import json
from typing import Any

from rich.console import Console
from rich.table import Table

console = Console()


def print_output(data: Any, json_output: bool = False) -> None:
    if json_output:
        print(json.dumps(data, default=_serialize, indent=2))
    else:
        _print_human(data)


def _serialize(obj: Any):
    """
    Fallback serializer for models.
    """
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    return str(obj)


def _print_human(data: Any) -> None:
    """
    Human-readable output.
    Start simple. Improve later.
    """
    if isinstance(data, list):
        table = Table(show_header=True, header_style="bold")
        table.add_column("Index")
        table.add_column("Value")

        for idx, item in enumerate(data):
            table.add_row(str(idx), str(item))

        console.print(table)
    else:
        console.print(data)
