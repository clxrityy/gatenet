"""
test_service_discovery.py
------------------------
Unit tests for ServiceDiscovery (unified protocol detection).
"""
import pytest
from gatenet.discovery.service_discovery import service_discovery, ServiceDiscovery

def test_detect_snmp_by_port():
    result = service_discovery.detect(161, "")
    assert result is not None
    assert result["protocol"] == "SNMP"
    assert result["detected"] is True

def test_detect_ldap_by_banner():
    result = service_discovery.detect(12345, "LDAP server ready")
    assert result is not None
    assert result["protocol"] == "LDAP"
    assert result["detected"] is True

def test_detect_coap_by_port():
    result = service_discovery.detect(5683, "")
    assert result is not None
    assert result["protocol"] == "CoAP"

def test_detect_mqtt_by_banner_case_insensitive():
    result = service_discovery.detect(9999, "MQTT Broker v5.0")
    assert result is not None
    assert result["protocol"] == "MQTT"

def test_detect_sip_by_port_and_banner():
    # By port
    result = service_discovery.detect(5060, "")
    assert result is not None
    assert result["protocol"] == "SIP"
    # By banner
    result2 = service_discovery.detect(1234, "SIP/2.0 200 OK")
    assert result2 is not None
    assert result2["protocol"] == "SIP"

def test_no_detection():
    result = service_discovery.detect(9999, "unknown service")
    assert result is None

def test_custom_protocol_registration():
    sd = ServiceDiscovery()
    sd.register_protocol("TESTPROTO", [4242], ["testproto"]) 
    # By port
    r1 = sd.detect(4242, "")
    assert r1 is not None and r1["protocol"] == "TESTPROTO"
    # By banner
    r2 = sd.detect(1, "TestProto Service Ready")
    assert r2 is not None and r2["protocol"] == "TESTPROTO"
