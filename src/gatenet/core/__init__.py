"""
Core utilities for extensibility and cross-module primitives.

Exports:
- Hooks: lightweight event bus for registering and emitting hooks.
- events: common event name constants.
"""

from .hooks import Hooks
from . import events

# Shared default hooks bus for the package
hooks = Hooks()

__all__ = [
    "Hooks",
    "events",
    "hooks",
]
