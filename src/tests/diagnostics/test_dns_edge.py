"""
Edge case tests for dns_lookup and reverse_dns_lookup.
"""
import pytest
from gatenet.diagnostics.dns import dns_lookup, reverse_dns_lookup

def test_dns_lookup_invalid():
    ip = dns_lookup("notarealdomain.tld")
    assert ip == "Unknown" or ip == "Invalid Hostname"

def test_reverse_dns_lookup_invalid():
    host = reverse_dns_lookup("256.256.256.256")
    assert host == "Unknown" or host == "Invalid IP"
