# CLI Examples

This directory contains examples demonstrating various CLI commands in the Gatenet library.

## Hotspot CLI Examples

### File: `hotspot_example.py`

This example demonstrates the hotspot management CLI commands including:

- **Password Generation**: Generate secure passwords for hotspots
- **Status Checking**: Check current hotspot status
- **Device Listing**: List connected devices
- **Help Commands**: Show available hotspot options

#### Usage

```bash
# Run the example
cd examples/cli
python3 hotspot_example.py
```

#### Example Commands Demonstrated

1. **Generate Secure Password (Table Format)**:

   ```bash
   python3 -m gatenet.cli hotspot generate-password --length 16 --output table
   ```

2. **Generate Password (JSON Format)**:

   ```bash
   python3 -m gatenet.cli hotspot generate-password --output json
   ```

3. **Check Hotspot Status**:

   ```bash
   python3 -m gatenet.cli hotspot status --output table
   ```

4. **List Connected Devices**:

   ```bash
   python3 -m gatenet.cli hotspot devices --output table
   ```

5. **Start a Hotspot** (requires root privileges):

   ```bash
   python3 -m gatenet.cli hotspot start --ssid MyHotspot --password securepass123 --security wpa2
   ```

6. **Stop a Hotspot** (requires root privileges):
   ```bash
   python3 -m gatenet.cli hotspot stop
   ```

#### Output Formats

All hotspot commands support multiple output formats:

- `table`: Human-readable table format (default)
- `json`: Machine-readable JSON format
- `plain`: Simple text format

#### Security Features

- Password generation with customizable length and complexity
- Support for WPA2/WPA3 security protocols
- Secure configuration validation
- Device monitoring and management

#### Requirements

- Root privileges for starting/stopping hotspots
- Appropriate network interfaces available
- Platform-specific hotspot capabilities

## Additional CLI Examples

More CLI examples will be added here as new commands are implemented.

### Future Examples

- Network diagnostics CLI examples
- Discovery service CLI examples
- HTTP client/server CLI examples
- Socket programming CLI examples

## Contributing

When adding new CLI examples:

1. Create a descriptive Python file in this directory
2. Include comprehensive comments and docstrings
3. Demonstrate multiple use cases and output formats
4. Update this README with the new example
5. Ensure examples follow security best practices
