from gatenet.core.models import Device


def test_device_str_representation():
    device = Device(
        ip="192.168.1.1",
        hostname="router",
    )

    s = str(device)

    assert "192.168.1.1" in s
    assert "router" in s
