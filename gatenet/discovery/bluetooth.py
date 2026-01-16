from gatenet.core.models import Device, Service
from gatenet.discovery.base import AsyncDiscoveryProvider

try:
    from bleak import BleakScanner
except ImportError:
    BleakScanner = None  # type: ignore


class BluetoothDiscovery(AsyncDiscoveryProvider):
    """BLE-based Bluetooth discovery provider.

    Discovers nearby Bluetooth Low Energy (BLE) devices via advertisements.

    Requires the `bleak` library. Install with the `bluetooth` extra:
        pip install gatenet[bluetooth]

    ```py
    bt_discovery = BluetoothDiscovery()
    ```
    """

    name = "bluetooth"
    async_capable = True

    async def discover_async(self) -> list[Device]:
        """Asynchronous Bluetooth device discovery implementation.

        Returns:
            A list of discovered Device instances.

        ```py
        devices = await bt_discovery.discover_async()
        ```
        """
        if BleakScanner is None:
            return []
        devices = await BleakScanner.discover()

        results: list[Device] = []

        for d in devices:
            # Device model is IP-first, so we store bluetooth identity
            # using services + metadata until Device evolves.
            device = Device(
                id=d.address,
                hostname=d.name,
                kind="bluetooth",
                transport="ble",
                services=[Service(name="bluetooth", ports=[])],
                metadata={
                    "bluetooth": {
                        "address": d.address,
                        "details": d.details,
                    }
                },
            )
            results.append(device)

        return results
