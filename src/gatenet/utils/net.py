import socket

def get_free_port():
    """
    Find and return a free TCP port on localhost.

    Returns
    -------
    int
        An available port number on localhost.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]