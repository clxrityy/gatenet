# Example script to demonstrate the use of get_geo_info function from gatenet.diagnostics

from gatenet.diagnostics import get_geo_info

def main():
    # Example IP addresses to test
    ip_addresses = [
        "8.8.8.8",  # Google Public DNS
        "1.1.1.1",  # Cloudflare Public DNS
        "2606:4700:4700::1111",  # Cloudflare IPv6 DNS
        "2001:4860:4860::8888",  # Google IPv6 DNS
    ]
    
    for ip in ip_addresses:
        try:
            geo_info = get_geo_info(ip)
            print(f"Geo info for {ip}:")
            print(f"  Country: {geo_info['country']}")
            print(f"  Region: {geo_info['region']}")
            print(f"  City: {geo_info['city']}")
            print(f"  Latitude: {geo_info['latitude']}")
            print(f"  Longitude: {geo_info['longitude']}")
        except Exception as e:
            print(f"Error retrieving geo info for {ip}: {e}")

if __name__ == "__main__":
    main()
# This script retrieves and prints geographical information for a list of IP addresses.
# It uses the get_geo_info function from the gatenet.diagnostics module.
# The output includes country, region, city, latitude, and longitude for each IP address.
# If an error occurs while retrieving geo info, it prints an error message.
# The script is designed to be run as a standalone program.