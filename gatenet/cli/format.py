"""
Output formatting utilities for the gatenet CLI.

This module is responsible for rendering command results to standard
output in either machine-readable (JSON) or human-readable formats.
It contains no discovery or scanning logic.
"""

import json
from typing import Any

from rich.console import Console
from rich.table import Table

console = Console()


def print_output(data: Any, json_output: bool = False) -> None:
    """
    Print command output to standard output.

    Depending on the selected format, this function either serializes
    data to JSON or renders a human-readable representation.

    Args:
        data: The data to output.
        json_output: If True, output data as formatted JSON.
    """
    if json_output:
        print(json.dumps(data, default=_serialize, indent=2))
    else:
        _print_human(data)


def _serialize(obj: Any):
    """
    Fallback JSON serializer for gatenet models.

    This function attempts to serialize objects by inspecting their
    instance dictionary. It is intended primarily for simple data
    models and should not be used for complex types.

    Args:
        obj: Object to serialize.

    Returns:
        A JSON-serializable representation of the object.
    """
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    return str(obj)


def _print_human(data: Any) -> None:
    """
    Render data in a human-readable format.

    This function provides a simple table-based output for iterable
    data and falls back to direct console printing for other types.
    The formatting is intentionally minimal and may evolve over time.

    Args:
        data: The data to render.
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
