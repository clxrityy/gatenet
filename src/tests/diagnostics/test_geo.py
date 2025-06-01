from gatenet.diagnostics import get_geo_info

def test_get_geo_info():
    # Test with a known IP address
    ip = "8.8.8.8"  # Google Public DNS
    geo_info = get_geo_info(ip)
    assert geo_info.get("country") == "United States", f"Expected IP to be {ip}, got {geo_info.get('ip')}"