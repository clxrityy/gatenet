import pytest
from gatenet.core.models import Device


@pytest.fixture
def sample_device() -> Device:
    return Device(
        ip="192.168.1.10",
        hostname="test-device",
    )
