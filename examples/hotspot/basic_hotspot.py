"""
Example usage of the gatenet.hotspot module.

This example demonstrates how to create and manage a Wi-Fi hotspot.
"""
from gatenet.hotspot import Hotspot, HotspotConfig, SecurityConfig, SecurityType
import time


def main():
    """Example hotspot creation and management."""
    print("Gatenet Hotspot Example")
    print("=" * 30)
    
    # Generate a strong password
    password = SecurityConfig.generate_password(12, include_symbols=True)
    print(f"Generated strong password: {password}")
    
    # Create security configuration
    security = SecurityConfig(password, SecurityType.WPA2)
    print(f"Security level: {security.get_security_level()}")
    print(f"Password valid: {security.validate_password()}")
    
    # Create hotspot configuration
    config = HotspotConfig(
        ssid="GatenetHotspot",
        password=password,
        interface="wlan0",  # Change to your wireless interface
        ip_range="192.168.4.0/24",
        gateway="192.168.4.1",
        channel=6,
        hidden=False
    )
    
    # Create and start hotspot
    print(f"\nCreating hotspot '{config.ssid}'...")
    hotspot = Hotspot(config)
    
    try:
        if hotspot.start():
            print("✓ Hotspot started successfully!")
            print(f"  SSID: {config.ssid}")
            print(f"  Password: {password}")
            print(f"  Gateway: {config.gateway}")
            print(f"  Channel: {config.channel}")
            
            # Monitor connected devices
            print("\nMonitoring connected devices...")
            for _ in range(10):  # Monitor for 10 iterations
                devices = hotspot.get_connected_devices()
                print(f"Connected devices: {len(devices)}")
                
                for device in devices:
                    print(f"  - {device['hostname']} ({device['ip']}) - {device['mac']}")
                
                time.sleep(5)  # Check every 5 seconds
                
        else:
            print("✗ Failed to start hotspot")
            print("  Make sure you have the required permissions and dependencies:")
            print("  - hostapd (Linux)")
            print("  - dnsmasq (Linux)")
            print("  - sudo privileges")
            
    except KeyboardInterrupt:
        print("\nShutting down...")
        
    finally:
        # Clean up
        if hotspot.stop():
            print("✓ Hotspot stopped successfully")
        else:
            print("✗ Error stopping hotspot")


def create_simple_hotspot():
    """Create a simple open hotspot for testing."""
    print("\nCreating simple open hotspot...")
    
    config = HotspotConfig(
        ssid="TestHotspot",
        password=None,  # Open network
        interface="wlan0"
    )
    
    hotspot = Hotspot(config)
    
    if hotspot.start():
        print("✓ Open hotspot started")
        time.sleep(10)  # Run for 10 seconds
        hotspot.stop()
        print("✓ Open hotspot stopped")
    else:
        print("✗ Failed to start open hotspot")


if __name__ == "__main__":
    # Run the main example
    main()
    
    # Uncomment to test simple open hotspot
    # create_simple_hotspot()
