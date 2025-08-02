"""
Gatenet CLI package entry point.

Usage:
    python -m gatenet.cli <command> [options]
    gatenet <command> [options] (if installed as a script)
"""
from .main import main

if __name__ == "__main__":
    main()
