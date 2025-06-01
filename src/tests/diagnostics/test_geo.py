from gatenet.diagnostics import get_geo_info

def test_get_geo_info():
    # Test with a known IP address
    ip = "8.8.8.8"  # Google Public DNS
    geo_info = get_geo_info(ip)
    assert geo_info.get("country") == "United States", f"Expected IP to be {ip}, got {geo_info.get('ip')}"

def test_get_geo_info_with_ipv6():
    # Test with a known IPv6 address
    ip = "2606:4700:4700::1111"  # Cloudflare IPv6 DNS
    geo_info = get_geo_info(ip)
    assert geo_info.get("country") == "Canada", f"Expected IP to be {ip}, got {geo_info.get('ip')}"
    
def test_get_geo_info_invalid_ip():
    # Test with an invalid IP address
    ip = "999.999.999.999"
    try:
        geo_info = get_geo_info(ip)
        assert geo_info["status"] == "fail", f"Expected status to be 'failed' for invalid IP, got {geo_info['status']}"
    except ValueError as e:
        assert str(e) == "Invalid IP address", f"Expected 'Invalid IP address' error, got {str(e)}"