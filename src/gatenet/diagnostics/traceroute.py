import socket
import time
from typing import List, Tuple, Optional

def _create_sockets(ttl: int, protocol: str, port: int, timeout: float):
    if protocol == "udp":
        send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        send_sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    else:  # ICMP
        send_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        send_sock.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    try:
        recv_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    except PermissionError:
        raise PermissionError("Raw sockets require admin/root privileges.")
    recv_sock.settimeout(timeout)
    recv_sock.bind(("0.0.0.0", port))
    return send_sock, recv_sock

def _send_probe(send_sock, dest_addr, protocol, port):
    if protocol == "udp":
        send_sock.sendto(b"", (dest_addr, port))
    else:
        icmp_packet = b'\x08\x00\x00\x00\x00\x00\x00\x00'  # Type 8, Code 0, rest is zero
        send_sock.sendto(icmp_packet, (dest_addr, 0))

def _receive_probe(recv_sock, start_time):
    try:
        _, curr = recv_sock.recvfrom(512)
        rtt = (time.time() - start_time) * 1000  # RTT in ms
        curr_addr = curr[0]
    except socket.timeout:
        curr_addr = "*"
        rtt = None
    return curr_addr, rtt

def _resolve_hostname(ip: str) -> str:
    if ip == "*":
        return ""
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return ""

def _print_hop(ttl: int, curr_addr: str, host_name: str, rtt: Optional[float]):
    display_addr = f"{curr_addr} ({host_name})" if host_name else curr_addr
    print(f"{ttl:2d}  {display_addr:20}  {f'{rtt:.2f} ms' if rtt is not None else '*'}")

def traceroute(
    host: str,
    max_hops: int = 30,
    timeout: float = 2.0,
    protocol: str = "udp",
    print_output: bool = True
) -> List[dict]:
    """
    Perform a traceroute to the given host using UDP or ICMP.

    Parameters
    ----------
    host : str
        The target hostname or IP address.
    max_hops : int, optional
        Maximum number of hops to trace (default: 30).
    timeout : float, optional
        Timeout in seconds for each probe (default: 2.0).
    protocol : {"udp", "icmp"}, optional
        Protocol to use for traceroute (default: "udp").
    print_output : bool, optional
        Whether to print each hop to stdout (default: True).

    Returns
    -------
    List[dict]
        List of hop info dicts with keys:
            - hop (int): The hop count (starting from 1).
            - ip (str): The IP address of the hop (or '*').
            - hostname (str): The resolved hostname (or '').
            - rtt_ms (Optional[float]): The round-trip time in ms, or None if timed out.

    Raises
    ------
    ValueError
        If the host cannot be resolved.
    PermissionError
        If raw sockets cannot be created (requires admin/root).

    Example
    -------
    >>> from gatenet.diagnostics.traceroute import traceroute
    >>> hops = traceroute("google.com", protocol="udp", print_output=False)
    >>> for hop in hops:
    ...     print(hop)
    {'hop': 1, 'ip': '192.168.1.1', 'hostname': 'router.local', 'rtt_ms': 2.34}
    ...
    """
    assert protocol in ("udp", "icmp"), "protocol must be 'udp' or 'icmp'"
    try:
        dest_addr = socket.gethostbyname(host)
    except socket.gaierror:
        raise ValueError(f"Unable to resolve host: {host}")

    port = 33434  # Default port used by traceroute
    result = []

    if print_output:
        print(f"Traceroute to {host} ({dest_addr}), {max_hops} hops max:")

    for ttl in range(1, max_hops + 1):
        send_sock, recv_sock = _create_sockets(ttl, protocol, port, timeout)
        start_time = time.time()
        try:
            _send_probe(send_sock, dest_addr, protocol, port)
            curr_addr, rtt = _receive_probe(recv_sock, start_time)
        finally:
            send_sock.close()
            recv_sock.close()

        host_name = _resolve_hostname(curr_addr)

        hop_info = {
            "hop": ttl,
            "ip": curr_addr,
            "hostname": host_name,
            "rtt_ms": rtt
        }
        if print_output:
            _print_hop(ttl, curr_addr, host_name, rtt)

        result.append(hop_info)

        if curr_addr == dest_addr:
            break

    return result