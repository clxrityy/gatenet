from gatenet.core.models import Device, Port, Service


# @pytest.fixture
def sample_device() -> Device:
    return Device(
        ip="192.168.1.10",
        hostname="test-device",
    )


# @pytest.fixture
def duplicate_device() -> Device:
    return Device(
        ip="192.168.1.10",
        hostname="",
        services=[Service(name="HTTP", ports=[Port(number=80)])],
    )
