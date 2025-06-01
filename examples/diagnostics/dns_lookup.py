# DNS Lookup Example
from gatenet.diagnostics import reverse_dns_lookup, dns_lookup

def main():
    # Example IP address for reverse DNS lookup
    ip_address = "1.1.1.1"  # Cloudflare's public DNS server
    hostname = reverse_dns_lookup(ip_address)
    print(f"Reverse DNS lookup for {ip_address}: {hostname}") # Expected: one.one.one.one
    
    # Example hostname for DNS lookup
    hostname = "www.cloudflare.com"
    ip = dns_lookup(hostname)
    print(f"DNS lookup for {hostname}: {ip}")  # Expected: 104.16.123.96