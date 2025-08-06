Hotspot Module
======================

The ``gatenet.hotspot`` module provides comprehensive Wi-Fi access point management capabilities for creating and controlling Wi-Fi hotspots on Linux and macOS systems.

Overview
--------

The hotspot module consists of four main components:

1. **Hotspot** - Main class for hotspot management
2. **HotspotConfig** - Configuration dataclass for hotspot settings  
3. **SecurityConfig** - Security and encryption management
4. **DHCPServer** - DHCP server for client IP assignment

Quick Start
-----------

.. code-block:: python

    from gatenet.hotspot import Hotspot, HotspotConfig

    # Create a basic secured hotspot
    config = HotspotConfig(
        ssid="MyHotspot",
        password="MySecurePassword123!"
    )

    hotspot = Hotspot(config)

    # Start the hotspot
    if hotspot.start():
        print("Hotspot started successfully!")
        
        # Get connected devices
        devices = hotspot.get_connected_devices()
        print(f"Connected devices: {devices}")
        
        # Stop the hotspot
        hotspot.stop()

Detailed Usage
--------------

Creating a Hotspot Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from gatenet.hotspot import HotspotConfig

    # Basic configuration
    config = HotspotConfig(ssid="MyNetwork")

    # Advanced configuration
    config = HotspotConfig(
        ssid="MyAdvancedNetwork",
        password="SecurePassword123!",
        interface="wlan0",           # Network interface
        ip_range="192.168.4.0/24",   # DHCP IP range
        gateway="192.168.4.1",       # Gateway IP
        channel=6,                   # Wi-Fi channel
        hidden=False                 # Broadcast SSID
    )

Security Configuration
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from gatenet.hotspot import SecurityConfig, SecurityType

    # Create security configuration
    security = SecurityConfig("MyPassword123!", SecurityType.WPA2)

    # Validate password strength
    if security.validate_password():
        print("Password is strong")
    else:
        print("Password is weak")

    # Generate a strong password
    strong_password = SecurityConfig.generate_password(16, include_symbols=True)

    # Get security level description
    level = security.get_security_level()  # "High (WPA2)"

DHCP Server Management
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from gatenet.hotspot import DHCPServer

    # Create DHCP server
    dhcp = DHCPServer(
        ip_range="192.168.4.0/24",
        gateway="192.168.4.1",
        dns_servers=["8.8.8.8", "1.1.1.1"]
    )

    # Start DHCP server
    if dhcp.start():
        print("DHCP server started")
        
    # Stop DHCP server
    dhcp.stop()

Open Network (No Security)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Create an open hotspot (no password required)
    config = HotspotConfig(
        ssid="OpenNetwork",
        password=None  # No password = open network
    )

    hotspot = Hotspot(config)
    hotspot.start()

Platform Support
----------------

Linux
~~~~~

- Uses ``hostapd`` for access point creation
- Uses ``dnsmasq`` for DHCP server
- Supports WPA2, WPA3, WEP, and open networks
- Requires root privileges (sudo)

macOS
~~~~~

- Uses system Internet Sharing functionality
- Built-in DHCP through system services
- Limited to system-supported security types

Requirements
~~~~~~~~~~~~

**Linux:**

.. code-block:: bash

    sudo apt-get install hostapd dnsmasq  # Ubuntu/Debian
    sudo yum install hostapd dnsmasq      # CentOS/RHEL

**macOS:**

- No additional packages required
- Uses built-in system functionality

Security Types
--------------

The module supports multiple security levels:

.. code-block:: python

    from gatenet.hotspot import SecurityType

    SecurityType.OPEN   # No encryption (not recommended)
    SecurityType.WEP    # WEP encryption (deprecated, avoid)
    SecurityType.WPA    # WPA encryption
    SecurityType.WPA2   # WPA2 encryption (recommended)
    SecurityType.WPA3   # WPA3 encryption (most secure)

Password Requirements
---------------------

For WPA/WPA2/WPA3 networks:

- Minimum 8 characters
- Maximum 63 characters
- Avoid common patterns (password123, qwerty, etc.)

The module provides automatic password validation and generation:

.. code-block:: python

    # Generate secure password
    password = SecurityConfig.generate_password(
        length=16,
        include_symbols=True
    )

    # Validate existing password
    config = SecurityConfig(password, SecurityType.WPA2)
    is_valid = config.validate_password()

Error Handling
--------------

The module includes comprehensive error handling:

.. code-block:: python

    try:
        hotspot = Hotspot(config)
        
        if not hotspot.start():
            print("Failed to start hotspot")
            
    except Exception as e:
        print(f"Error: {e}")

Common issues:

- Insufficient privileges (need sudo on Linux)
- Network interface not available
- Conflicting network services
- Weak password for secured networks

Advanced Features
-----------------

Custom DHCP Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    config = HotspotConfig(
        ssid="CustomDHCP",
        password="SecurePass123!",
        ip_range="10.0.0.0/24",      # Custom IP range
        gateway="10.0.0.1"           # Custom gateway
    )

    hotspot = Hotspot(config)

    # Access DHCP server directly
    dhcp = hotspot.dhcp_server
    dhcp.dns_servers = ["1.1.1.1", "1.0.0.1"]  # Custom DNS

Monitor Connected Devices
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Get list of connected devices
    devices = hotspot.get_connected_devices()

    for device in devices:
        print(f"Device: {device}")

Hotspot Status
~~~~~~~~~~~~~~

.. code-block:: python

    # Check if hotspot is running
    if hotspot.is_running:
        print("Hotspot is active")
        
    # Get security information
    if hotspot.security:
        print(f"Security: {hotspot.security.get_security_level()}")

Configuration Examples
----------------------

Enterprise-style Hotspot
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    config = HotspotConfig(
        ssid="CompanyGuest",
        password="Enterprise2024!",
        interface="wlan0",
        ip_range="172.16.0.0/24",
        gateway="172.16.0.1",
        channel=11,
        hidden=False
    )

    # Use WPA3 for maximum security
    hotspot = Hotspot(config)
    hotspot.security.security_type = SecurityType.WPA3

Development/Testing Hotspot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    config = HotspotConfig(
        ssid="DevTest",
        password="DevPassword123",
        channel=1  # Avoid interference on crowded channels
    )

    hotspot = Hotspot(config)

Public Open Hotspot
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    config = HotspotConfig(
        ssid="PublicWiFi",
        password=None,  # Open network
        ip_range="192.168.10.0/24"
    )

    hotspot = Hotspot(config)

Best Practices
--------------

1. **Security**: Always use WPA2 or WPA3 for production networks
2. **Passwords**: Use generated passwords with mixed characters
3. **Channels**: Choose less congested Wi-Fi channels (1, 6, 11 for 2.4GHz)
4. **IP Ranges**: Use private IP ranges (192.168.x.x, 10.x.x.x, 172.16.x.x)
5. **Monitoring**: Regularly check connected devices
6. **Cleanup**: Always stop hotspots when done

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Permission denied:**

.. code-block:: bash

    sudo python your_script.py  # Run with sudo on Linux

**Interface busy:**

.. code-block:: python

    # Check if interface is already in use
    # Stop conflicting services: NetworkManager, wpa_supplicant

**DHCP conflicts:**

.. code-block:: python

    # Use different IP ranges to avoid conflicts
    config.ip_range = "192.168.100.0/24"

**Weak password error:**

.. code-block:: python

    # Use stronger passwords
    password = SecurityConfig.generate_password(16)

Integration with Other Modules
------------------------------

The hotspot module integrates well with other ``gatenet`` modules:

.. code-block:: python

    from gatenet.diagnostics import ping
    from gatenet.hotspot import Hotspot, HotspotConfig

    # Create hotspot
    config = HotspotConfig(ssid="TestNet", password="TestPass123!")
    hotspot = Hotspot(config)
    hotspot.start()

    # Test connectivity
    result = ping("8.8.8.8")
    print(f"Internet connectivity: {result.success}")

    # Monitor clients
    devices = hotspot.get_connected_devices()
    for device in devices:
        # Ping each connected device
        ping_result = ping(device.ip)
        print(f"Device {device.mac}: {ping_result.avg_rtt}ms")

