from gatenet.diagnostics import check_public_port, scan_ports, check_port, scan_ports_async
import pytest

def test_well_known_dns_server():
    # Cloudflare DNS server should always be reachable on port 53
    result = check_public_port("1.1.1.1", 53)
    assert isinstance(result, bool)
    
def test_scan_ports():
    # Scan a few well-known ports on localhost
    results = scan_ports("127.0.0.1")
    assert isinstance(results, list)
    assert all(isinstance(t, tuple) and len(t) == 2 for t in results)
    assert all(isinstance(t[0], int) and isinstance(t[1], bool) for t in results)

@pytest.mark.asyncio
async def test_check_port():
    port, is_open = await check_port("1.1.1.1", 53)
    assert isinstance(port, int)
    assert isinstance(is_open, bool)

@pytest.mark.asyncio
async def test_scan_ports_async():
    results = await scan_ports_async("127.0.0.1")
    assert isinstance(results, list)
    assert all(isinstance(res, tuple) and len(res) == 2 for res in results), "Results should be a list of tuples (port, is_open)"
    assert all(isinstance(res[0], int) and isinstance(res[1], bool) for res in results)