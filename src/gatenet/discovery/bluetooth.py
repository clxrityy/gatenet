from typing import Dict, List
import asyncio
from bleak import BleakScanner


def discover_bluetooth_devices(timeout: float = 8.0) -> List[Dict[str, str]]:
    """
    Scan for nearby Bluetooth devices.

    Parameters
    ----------
    timeout : float, optional
        Time to scan in seconds (default is 8.0).

    Returns
    -------
    List[Dict[str, str]]
        List of discovered device dictionaries.

    Raises
    ------
    Exception
        If an error occurs during Bluetooth discovery (caught and printed, returns empty list).

    Example
    -------
    >>> from gatenet.discovery.bluetooth import discover_bluetooth_devices
    >>> devices = discover_bluetooth_devices(timeout=4.0)
    >>> for device in devices:
    ...     print(device)
    {'address': '00:1A:7D:DA:71:13', 'name': 'MyBluetoothDevice'}
    """
    import logging
    try:
        # Pass timeout to the async function via a closure or global if needed
        return asyncio.run(_async_discover_bluetooth_devices())
    except Exception as e:
        logging.error(f"Error during Bluetooth discovery: {e}")
        return [{"error": str(e)}]

async def _async_discover_bluetooth_devices() -> List[Dict[str, str]]:
    """
    Asynchronously scan for nearby Bluetooth devices using a timeout context manager.

    Returns
    -------
    List[Dict[str, str]]
        List of discovered device dictionaries.

    Raises
    ------
    Exception
        If an error occurs during async Bluetooth scan (caught and printed, returns empty list).
    """
    devices = []
    timeout = 8.0  # Default timeout, can be adjusted by caller if needed

    try:
        discovered_devices = await asyncio.wait_for(
            BleakScanner.discover(return_adv=True),
            timeout=timeout
        )

        for device_with_adv in discovered_devices.values():
            device = device_with_adv[0]
            advertisement_data = device_with_adv[1]
            device_info = {
                "address": device.address,
                "name": device.name or "Unknown Device",
                "rssi": str(advertisement_data.rssi) if advertisement_data.rssi else "N/A"
            }

            # Add service UUIDs if available
            if advertisement_data.service_uuids:
                device_info["services"] = ", ".join(str(uuid) for uuid in advertisement_data.service_uuids)

            # Add manufacturer data if available
            if advertisement_data.manufacturer_data:
                manufacturer_info = []
                for manufacturer_id, data in advertisement_data.manufacturer_data.items():
                    manufacturer_info.append(f"{manufacturer_id}: {data.hex()}")
                device_info["manufacturer_data"] = ", ".join(manufacturer_info)

            devices.append(device_info)

    except Exception as e:
        import logging
        logging.error(f"Error during async Bluetooth scan: {e}")
        return [{"error": str(e)}]
    return devices

async def async_discover_bluetooth_devices() -> List[Dict[str, str]]:
    """
    Asynchronously scan for nearby Bluetooth devices.

    :return: List of discovered device dictionaries.
    """
    return await _async_discover_bluetooth_devices()