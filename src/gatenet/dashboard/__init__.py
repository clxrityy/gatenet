"""
Gatenet Dashboard
-----------------
A modern, extensible web dashboard for diagnostics, service discovery, and monitoring.

This module provides a FastAPI-based dashboard for Gatenet, with a public API for launching the app.
"""

from .app import launch_dashboard

__all__ = ["launch_dashboard"]
