import pytest
from gatenet.service_detectors.mqtt import MQTTDetector

@pytest.mark.parametrize("port,banner,expected", [
    (1883, "MQTT Broker Ready", "MQTT Broker"),
    (1883, "mqtt", "MQTT Broker"),
    (80, "mqtt", "MQTT Broker"),
    (1883, "", None),
    (80, "", None),
])
def test_mqtt_detector(port, banner, expected):
    detector = MQTTDetector()
    assert detector.detect(port, banner) == expected
