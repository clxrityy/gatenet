"""
mqtt.py
-------
Service detection strategy for MQTT protocol.

Public API:
    - MQTTDetector
"""
from typing import Optional
from gatenet.service_detectors import ServiceDetector

class MQTTDetector(ServiceDetector):
    """
    Service detector for MQTT brokers.
    Detects MQTT brokers from port and banner.
    """
    def detect(self, port: int, banner: str) -> Optional[str]:
        if port != 1883 and 'mqtt' not in banner.lower():
            return None
        if 'mqtt' in banner.lower():
            return "MQTT Broker"
        return None
