import socket

def reverse_dns_lookup(ip: str) -> str:
    """
    Perform a reverse DNS lookup for a given IP address.

    :param ip: The IP address to look up.
    :return: The hostname associated with the IP address, or 'Unknown' if not found.
    """
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "Unknown"
    except socket.gaierror:
        return "Invalid IP"  # Handle invalid IP addresses gracefully

def dns_lookup(hostname: str) -> str:
    """
    Perform a DNS lookup for a given hostname.

    :param hostname: The hostname to look up.
    :return: The IP address associated with the hostname, or 'Unknown' if not found.
    """
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return "Unknown"
    except socket.herror:
        return "Invalid Hostname"  # Handle invalid hostnames gracefully