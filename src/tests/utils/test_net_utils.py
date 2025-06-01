from gatenet.utils import get_free_port

def test_get_free_port():
    port = get_free_port()
    assert 1024 <= port <= 65535