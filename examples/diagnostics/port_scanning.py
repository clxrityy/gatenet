# Port scanning example
from gatenet.diagnostics import check_public_port, scan_ports, check_port, scan_ports_async

async def main():
    # Check if a public port is open
    ip_address = "1.1.1.1"  # Cloudflare's public DNS server
    target_port = 53  # DNS port
    is_open = check_public_port(ip_address, target_port)
    print(f"Port {target_port} on {ip_address} is {'open' if is_open else 'closed'}")

    # Scan a range of ports on localhost
    localhost = "127.0.0.1"
    ports = [22, 80, 443]
    open_ports = scan_ports(localhost, ports)
    print(f"Open ports on {localhost}: {open_ports}")
    
    # Check a specific port on a given IP address
    # Get the port status asynchronously
    port, is_open = await check_port(ip_address, target_port)
    print(f"Port {port} on {ip_address} is {'open' if is_open else 'closed'}")
    
    # Scan ports asynchronously
    # Ports default to common ports if not specified
    results = await scan_ports_async(localhost)
    print(f"Async scan results for {localhost}: {results}")
    