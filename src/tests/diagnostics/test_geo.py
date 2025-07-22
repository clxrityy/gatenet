from gatenet.diagnostics import get_geo_info

def test_get_geo_info():
    # Test with a known IP address
    ip = "8.8.8.8"  # Google Public DNS
    geo_info = get_geo_info(ip)
    assert isinstance(geo_info, dict)
    if geo_info.get("error"):
        # Acceptable if API rate-limited or network error
        assert "message" in geo_info
    else:
        assert geo_info.get("country") in ("United States", "US"), f"Expected country for {ip}, got {geo_info.get('country')}"

def test_get_geo_info_with_ipv6():
    # Test with a known IPv6 address
    ip = "2606:4700:4700::1111"  # Cloudflare IPv6 DNS
    geo_info = get_geo_info(ip)
    assert isinstance(geo_info, dict)
    if geo_info.get("error"):
        assert "message" in geo_info
    else:
        # Accept either US or Canada, as geo IPs can change
        assert geo_info.get("country") in ("United States", "Canada", "US", "CA"), f"Expected country for {ip}, got {geo_info.get('country')}"
    
def test_get_geo_info_invalid_ip():
    # Test with an invalid IP address
    ip = "999.999.999.999"
    geo_info = get_geo_info(ip)
    assert isinstance(geo_info, dict)
    assert geo_info.get("error") is True
    assert geo_info.get("status") == "fail"
    assert geo_info.get("query") == ip