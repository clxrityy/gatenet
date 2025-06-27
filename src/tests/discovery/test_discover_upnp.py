# src/tests/discovery/test_discover_upnp.py

import socket
import pytest
from unittest.mock import patch, MagicMock

from gatenet.discovery.upnp import discover_upnp_devices

@pytest.fixture
def mock_ssdp_response():
    return (
        b"HTTP/1.1 200 OK\r\n"
        b"LOCATION: http://192.168.1.1:1900/device.xml\r\n"
        b"ST: upnp:rootdevice\r\n"
        b"USN: uuid:device-UUID::upnp:rootdevice\r\n"
        b"SERVER: Custom/1.0 UPnP/1.0 Proc/Ver\r\n"
        b"\r\n"
    )

@patch("socket.socket")
def test_discover_upnp_devices_mocked(mock_socket_class, mock_ssdp_response):
    # Mock socket instance
    mock_socket = MagicMock()
    mock_socket.recvfrom.side_effect = [
        (mock_ssdp_response, ("192.168.1.1", 1900)),
        socket.timeout("timed out")
    ]
    mock_socket_class.return_value = mock_socket

    devices = discover_upnp_devices(timeout=1.0)

    assert isinstance(devices, list)
    assert len(devices) == 1

    device = devices[0]
    assert device["LOCATION"] == "http://192.168.1.1:1900/device.xml"
    assert device["ST"] == "upnp:rootdevice"
    assert device["USN"] == "uuid:device-UUID::upnp:rootdevice"
    assert device["SERVER"] == "Custom/1.0 UPnP/1.0 Proc/Ver"
