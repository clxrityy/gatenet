#!/usr/bin/env python3
"""
Example: Hotspot CLI Usage
Demonstrates various hotspot management commands.
"""

import subprocess
import sys
import time

# CLI command constants
CLI_MODULE = "gatenet.cli"
CLI_BASE = ["python3", "-m", CLI_MODULE, "hotspot"]

def run_command(cmd):
    """Run a CLI command and display the output."""
    print(f"\n🔧 Running: {' '.join(cmd)}")
    print("=" * 60)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print(f"⚠️  Stderr: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stdout:
            print(f"Stdout: {e.stdout}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")

def main():
    """Demonstrate hotspot CLI commands."""
    print("🌐 Gatenet Hotspot CLI Examples")
    print("=" * 60)
    
    # Generate a secure password
    print("\n1. Generate a secure password:")
    run_command(CLI_BASE + ["generate-password", "--length", "16", "--output", "table"])
    
    # Generate password in JSON format
    print("\n2. Generate password (JSON format):")
    run_command(CLI_BASE + ["generate-password", "--output", "json"])
    
    # Check hotspot status
    print("\n3. Check hotspot status:")
    run_command(CLI_BASE + ["status", "--output", "table"])
    
    # Check status in JSON format
    print("\n4. Check status (JSON format):")
    run_command(CLI_BASE + ["status", "--output", "json"])
    
    # List connected devices
    print("\n5. List connected devices:")
    run_command(CLI_BASE + ["devices", "--output", "table"])
    
    # Show help for hotspot command
    print("\n6. Hotspot command help:")
    run_command(CLI_BASE + ["--help"])
    
    print("\n" + "=" * 60)
    print("💡 Example hotspot start command (not executed for safety):")
    print(f"   python3 -m {CLI_MODULE} hotspot start --ssid MyHotspot --password securepass123 --security wpa2")
    print(f"   python3 -m {CLI_MODULE} hotspot stop")
    print("\n⚠️  Note: Starting/stopping hotspots requires root privileges and proper network interfaces.")
    print("    These commands are not executed in this example for safety reasons.")

if __name__ == "__main__":
    main()
