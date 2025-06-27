import pytest
from unittest.mock import patch, MagicMock
from gatenet.discovery.mdns import discover_mdns_services, MDNSListener


@pytest.fixture
def mock_service_info():
    mock_info = MagicMock()
    mock_info.parsed_addresses.return_value = ["192.168.1.42"]
    mock_info.port = 8080
    mock_info.server = "test-device.local."
    mock_info.properties = {
        b"version": b"1.0",
        b"platform": b"gatenet"
    }
    return mock_info


@patch("gatenet.discovery.mdns.ServiceBrowser")
@patch("gatenet.discovery.mdns.Zeroconf")
def test_discover_mdns_services_mocked(mock_zeroconf_class, mock_service_browser, mock_service_info):
    # Create mock Zeroconf instance
    mock_zc = MagicMock()
    mock_zc.get_service_info.return_value = mock_service_info
    mock_zeroconf_class.return_value = mock_zc

    # Replace listener with one we can trigger manually
    _ = MDNSListener()
    mock_service_type = "_http._tcp.local."
    mock_service_name = "TestService._http._tcp.local."

    # Inject listener and simulate add_service call
    mock_service_browser.side_effect = lambda zc, type_, l: l.add_service(zc, mock_service_type, mock_service_name)

    # Run
    services = discover_mdns_services(timeout=0.1)

    # Assertions
    assert isinstance(services, list)
    assert len(services) == 1
    assert services[0]["address"] == "192.168.1.42"
    assert services[0]["port"] == "8080"
    assert services[0]["server"] == "test-device.local."
    assert "properties" in services[0]
