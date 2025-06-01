from gatenet.diagnostics import reverse_dns_lookup, dns_lookup

def test_reverse_dns_lookup():
    # Test with a known IP address
    ip = "1.1.1.1"  # Cloudflare's public DNS server
    hostname = reverse_dns_lookup(ip)
    assert hostname == "one.one.one.one", f"Expected hostname for {ip} to be 'one.one.one.one', got {hostname}"
    
def test_reverse_dns_lookup_invalid_ip():
    # Test with an invalid IP address
    ip = "999.999.999.999"
    hostname = reverse_dns_lookup(ip)
    assert hostname == "Invalid IP", f"Expected hostname for {ip} to be 'Invalid IP', got {hostname}"
    
def test_dns_lookup():
    # Test with a known hostname
    hostname = "www.cloudflare.com"
    ip = dns_lookup(hostname)
    assert ip in ["104.16.123.96", "104.16.124.96"], f"Expected IP for {hostname} to be '104.16.123.96', got {ip}"