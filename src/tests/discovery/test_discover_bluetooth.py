import pytest
from unittest.mock import patch, AsyncMock
from gatenet.discovery.bluetooth import discover_bluetooth_devices, async_discover_bluetooth_devices


class TestBluetoothDiscovery:
    """Test suite for Bluetooth device discovery functions."""

    @pytest.mark.asyncio
    async def test_async_discover_bluetooth_devices_success(self):
        """Test successful asynchronous Bluetooth device discovery."""
        mock_result = [{
            "address": "11:22:33:44:55:66",
            "name": "Async Test Device",
            "rssi": "-65",
            "services": "180a"
        }]
        
        with patch('gatenet.discovery.bluetooth._async_discover_bluetooth_devices', new_callable=AsyncMock) as mock_discover:
            mock_discover.return_value = mock_result
            
            result = await async_discover_bluetooth_devices()
            
            assert len(result) == 1
            assert result[0]["address"] == "11:22:33:44:55:66"
            assert result[0]["name"] == "Async Test Device"
            assert result[0]["rssi"] == "-65"
            assert result[0]["services"] == "180a"

    @pytest.mark.asyncio
    async def test_async_discover_bluetooth_devices_unknown_device(self):
        """Test handling of devices with no name."""
        mock_result = [{
            "address": "AA:BB:CC:DD:EE:FF",
            "name": "Unknown Device",
            "rssi": "-40"
        }]
        
        with patch('gatenet.discovery.bluetooth._async_discover_bluetooth_devices', new_callable=AsyncMock) as mock_discover:
            mock_discover.return_value = mock_result
            
            result = await async_discover_bluetooth_devices()
            
            assert len(result) == 1
            assert result[0]["name"] == "Unknown Device"
            assert result[0]["address"] == "AA:BB:CC:DD:EE:FF"

    @pytest.mark.asyncio
    async def test_async_discover_bluetooth_devices_no_rssi(self):
        """Test handling of devices with no RSSI data."""
        mock_result = [{
            "address": "FF:EE:DD:CC:BB:AA",
            "name": "No RSSI Device",
            "rssi": "N/A"
        }]
        
        with patch('gatenet.discovery.bluetooth._async_discover_bluetooth_devices', new_callable=AsyncMock) as mock_discover:
            mock_discover.return_value = mock_result
            
            result = await async_discover_bluetooth_devices()
            
            assert len(result) == 1
            assert result[0]["rssi"] == "N/A"

    @pytest.mark.asyncio
    async def test_async_discover_bluetooth_devices_with_manufacturer_data(self):
        """Test handling of devices with manufacturer data."""
        mock_result = [{
            "address": "12:34:56:78:9A:BC",
            "name": "Manufacturer Device",
            "rssi": "-55",
            "manufacturer_data": "76: 02151234, 6: ffeedd"
        }]
        
        with patch('gatenet.discovery.bluetooth._async_discover_bluetooth_devices', new_callable=AsyncMock) as mock_discover:
            mock_discover.return_value = mock_result
            
            result = await async_discover_bluetooth_devices()
            
            assert len(result) == 1
            assert "manufacturer_data" in result[0]
            manufacturer_data = result[0]["manufacturer_data"]
            assert "76: 02151234" in manufacturer_data
            assert "6: ffeedd" in manufacturer_data

    @pytest.mark.asyncio
    async def test_async_discover_bluetooth_devices_empty_results(self):
        """Test handling when no devices are discovered."""
        with patch('gatenet.discovery.bluetooth._async_discover_bluetooth_devices', new_callable=AsyncMock) as mock_discover:
            mock_discover.return_value = []
            
            result = await async_discover_bluetooth_devices()
            
            assert result == []

    @pytest.mark.asyncio
    async def test_async_discover_bluetooth_devices_exception(self):
        """Test async discovery handles exceptions gracefully."""
        # Mock the BleakScanner.discover to raise an exception
        # This tests the exception handling within _async_discover_bluetooth_devices
        with patch('gatenet.discovery.bluetooth.BleakScanner.discover', new_callable=AsyncMock) as mock_discover:
            mock_discover.side_effect = Exception("Bluetooth scan failed")
            
            result = await async_discover_bluetooth_devices()
            
            # The function should handle the exception and return an empty list
            assert result == []

    @pytest.mark.asyncio
    async def test_async_discover_bluetooth_devices_multiple_devices(self):
        """Test discovery of multiple devices."""
        mock_result = [
            {
                "address": "AA:BB:CC:DD:EE:01",
                "name": "Device One",
                "rssi": "-30",
                "services": "180f"
            },
            {
                "address": "AA:BB:CC:DD:EE:02",
                "name": "Device Two",
                "rssi": "-70",
                "services": "1805, 180a",
                "manufacturer_data": "76: 0102"
            }
        ]
        
        with patch('gatenet.discovery.bluetooth._async_discover_bluetooth_devices', new_callable=AsyncMock) as mock_discover:
            mock_discover.return_value = mock_result
            
            result = await async_discover_bluetooth_devices()
            
            assert len(result) == 2
            
            # Check devices by looking at addresses
            addresses = [device["address"] for device in result]
            assert "AA:BB:CC:DD:EE:01" in addresses
            assert "AA:BB:CC:DD:EE:02" in addresses
            
            # Find specific devices
            device1 = next((d for d in result if d["address"] == "AA:BB:CC:DD:EE:01"), None)
            device2 = next((d for d in result if d["address"] == "AA:BB:CC:DD:EE:02"), None)
            
            assert device1 is not None
            assert device1["name"] == "Device One"
            assert device1["services"] == "180f"
            
            assert device2 is not None
            assert device2["name"] == "Device Two"
            assert device2["services"] == "1805, 180a"
            assert "manufacturer_data" in device2

    def test_discover_bluetooth_devices_success(self):
        """Test successful synchronous Bluetooth device discovery."""
        expected_result = [{
            "address": "AA:BB:CC:DD:EE:FF",
            "name": "Test Device",
            "rssi": "-50",
            "services": "180f, 1805"
        }]
        
        with patch('gatenet.discovery.bluetooth.asyncio.run') as mock_asyncio_run:
            mock_asyncio_run.return_value = expected_result
            
            result = discover_bluetooth_devices(timeout=5.0)
            
            assert result == expected_result
            mock_asyncio_run.assert_called_once()

    def test_discover_bluetooth_devices_exception(self):
        """Test synchronous discovery handles exceptions gracefully."""
        with patch('gatenet.discovery.bluetooth.asyncio.run') as mock_asyncio_run:
            mock_asyncio_run.side_effect = Exception("Bluetooth adapter not found")
            
            result = discover_bluetooth_devices()
            
            assert result == []
            mock_asyncio_run.assert_called_once()

    def test_discover_bluetooth_devices_default_timeout(self):
        """Test that default timeout is used when not specified."""
        with patch('gatenet.discovery.bluetooth.asyncio.run') as mock_asyncio_run:
            mock_asyncio_run.return_value = []
            
            discover_bluetooth_devices()
            
            mock_asyncio_run.assert_called_once()