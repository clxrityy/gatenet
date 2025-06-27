# Bluetooth device discovery example
from gatenet.discovery.bluetooth import discover_bluetooth_devices, async_discover_bluetooth_devices

# Synchronous usage:
devices = discover_bluetooth_devices(timeout=10.0)
for device in devices:
    print(f"Found: {device['name']} ({device['address']}) - RSSI: {device['rssi']}")
    
# Asynchronous usage:
async def main():
    devices = await async_discover_bluetooth_devices()
    for device in devices:
        print(f"Found: {device['name']} ({device['address']}) - RSSI: {device['rssi']}")