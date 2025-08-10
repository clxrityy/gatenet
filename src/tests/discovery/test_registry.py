import pytest

from gatenet.discovery import (
    register_detector,
    register_detectors,
    clear_detectors,
    get_detectors,
)
from gatenet.discovery.detectors import (
    ServiceDetector,
    SSHDetector,
    HTTPDetector,
    FallbackDetector,
)
from gatenet.discovery.ssh import _identify_service


class DummyDetector(ServiceDetector):
    def __init__(self, name: str = "Dummy"):
        self.name = name

    def detect(self, port: int, banner: str):
        # Always match for predictability in tests
        return f"{self.name} Service"


@pytest.fixture(autouse=True)
def reset_registry():
    # Ensure a clean default registry before and after each test
    clear_detectors(keep_defaults=True)
    try:
        yield
    finally:
        clear_detectors(keep_defaults=True)


def test_default_registry_shape():
    detectors = get_detectors()
    assert isinstance(detectors[0], SSHDetector)
    assert isinstance(detectors[1], HTTPDetector)
    assert isinstance(detectors[-1], FallbackDetector)


def test_register_detector_insert_near_start():
    d = DummyDetector("Custom1")
    register_detector(d, append=False)
    detectors = get_detectors()
    # Inserted after SSH and HTTP
    assert isinstance(detectors[0], SSHDetector)
    assert isinstance(detectors[1], HTTPDetector)
    assert isinstance(detectors[2], DummyDetector)
    assert isinstance(detectors[-1], FallbackDetector)

    # Should be picked first by identify due to early insertion
    result = _identify_service(9999, "anything")
    assert result == "Custom1 Service"


def test_register_detectors_appends_before_fallback():
    d1 = DummyDetector("A")
    d2 = DummyDetector("B")
    register_detectors([d1, d2])
    detectors = get_detectors()
    # Fallback must remain last
    assert isinstance(detectors[-1], FallbackDetector)
    # The last two before fallback should be our custom detectors in order
    assert isinstance(detectors[-3], DummyDetector)
    assert detectors[-3].name == "A"
    assert isinstance(detectors[-2], DummyDetector)
    assert detectors[-2].name == "B"


def test_clear_detectors_empty_then_unknown_service():
    clear_detectors(keep_defaults=False)
    detectors = get_detectors()
    assert detectors == []
    # With empty registry, identify should still return an Unknown string
    res = _identify_service(12345, "")
    assert res.startswith("Unknown Service (Port ")
