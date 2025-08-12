"""
Gatenet CLI package entry point.

Usage:
    python -m gatenet.cli <command> [options]
    gatenet <command> [options] (if installed as a script)
"""
from .main import main
import sys

if __name__ == "__main__":
    sys.exit(main())
