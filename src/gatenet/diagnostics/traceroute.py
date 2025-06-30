import socket
import time
from typing import List, Tuple, Optional

def traceroute(
    host: str,
    max_hops: int = 30,
    timeout: float = 2.0
) -> List[Tuple[int, str, Optional[float]]]:
    """
    Perform a synchronous traceroute to the given host.

    Args:
        host (str): The target hostname or IP address.
        max_hops (int): Maximum number of hops to trace (default: 30).
        timeout (float): Timeout in seconds for each probe (default: 2.0).

    Returns:
        List[Tuple[int, str, Optional[float]]]: A list of (hop_number, ip, rtt_ms) tuples.
            - hop_number (int): The hop count (starting from 1).
            - ip (str): The IP address of the hop (or '*' if not found).
            - rtt_ms (Optional[float]): The round-trip time in milliseconds, or None if timed out.
    """
    # Try to resolve the host to an IP address
    try:
        dest_addr = socket.gethostbyname(host)
    except socket.gaierror:
        raise ValueError(f"Unable to resolve host: {host}")

    port = 33434  # Default port used by traceroute
    result = []

    print(f"Traceroute to {host} ({dest_addr}), {max_hops} hops max:")

    for ttl in range(1, max_hops + 1):
        # Create a UDP socket for sending packets
        send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        send_sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        # Create a raw socket to receive ICMP responses
        recv_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        recv_sock.settimeout(timeout)
        recv_sock.bind(("127.0.0.1", port))

        # Send a UDP packet to the destination
        start_time = time.time()
        try:
            send_sock.sendto(b"", (dest_addr, port))
            curr_addr = None
            rtt = None

            try:
                # Wait for an ICMP response
                _, curr = recv_sock.recvfrom(512)
                rtt = (time.time() - start_time) * 1000  # RTT in ms
                curr_addr = curr[0]
            except socket.timeout:
                curr_addr = "*"
                rtt = None
        finally:
            send_sock.close()
            recv_sock.close()

        # Try to resolve the hostname for the hop (optional)
        try:
            host_name = socket.gethostbyaddr(curr_addr)[0] if curr_addr != "*" else ""
        except Exception:
            host_name = ""

        display_addr = f"{curr_addr} ({host_name})" if host_name else curr_addr
        print(f"{ttl:2d}  {display_addr:20}  {f'{rtt:.2f} ms' if rtt is not None else '*'}")

        result.append((ttl, curr_addr, rtt))

        # Stop if we've reached the destination
        if curr_addr == dest_addr:
            break

    return result