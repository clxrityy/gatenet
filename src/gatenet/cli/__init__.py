"""
Gatenet CLI package.

This package exposes the CLI entry point used by the installed `gatenet` script.
Use `python -m gatenet.cli` or `gatenet` after installing the package.
"""

from .main import main

__all__ = ["main"]
