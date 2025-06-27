from gatenet.discovery.mdns import discover_mdns_services, MDNSListener

def main():
    print("Discovering mDNS services on the local network...")
    services = discover_mdns_services(timeout=3.0)

    if not services:
        print("No services found.")
        return

    for i, service in enumerate(services, 1):
        print(f"\nService #{i}")
        print(f"Name:     {service.get('name')}")
        print(f"Type:     {service.get('type')}")
        print(f"Address:  {service.get('address')}")
        print(f"Port:     {service.get('port')}")
        print(f"Server:   {service.get('server')}")
        if 'properties' in service:
            print(f"Props:    {service['properties']}")

if __name__ == "__main__":
    main()
# This script will discover mDNS services on the local network and print their details.
# It uses the `discover_mdns_services` function from the gatenet.diagnostics.mdns