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

def test_dns_lookup_unresolvable():
    # Test with a gibberish domain
    hostname = "nonexistentdomain1234567890.com"
    ip = dns_lookup(hostname)
    assert ip == "Unknown", f"Expected 'Unknown' for unresolvable hostname, got {ip}"

def test_dns_lookup_empty():
    # Test with empty string
    ip = dns_lookup("")
    assert ip in ["Unknown", "Invalid Hostname", "0.0.0.0"], f"Expected 'Unknown', 'Invalid Hostname', or '0.0.0.0' for empty hostname, got {ip}"

def test_reverse_dns_lookup_ipv6():
    # Test with a valid IPv6 address (may return Unknown if not mapped)
    ip = "2606:4700:4700::1111"  # Cloudflare IPv6
    hostname = reverse_dns_lookup(ip)
    assert hostname == "Unknown" or isinstance(hostname, str), f"Expected string for IPv6 reverse lookup, got {hostname}"

def test_dns_lookup_no_a_record():
    # Test with a hostname that likely has no A record (use a reserved TLD)
    hostname = "example.invalid"
    ip = dns_lookup(hostname)
    assert ip == "Unknown", f"Expected 'Unknown' for hostname with no A record, got {ip}"