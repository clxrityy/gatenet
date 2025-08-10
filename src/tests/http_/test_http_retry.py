import time
import socket
import urllib.error
import urllib.request

from gatenet.http_.server import HTTPServerComponent
from gatenet.utils import get_free_port


def _retry_get(url: str, max_retries: int = 3, delay: float = 0.05) -> bytes:
    """
    Simple retry helper: retries on HTTP 5xx, URLError, or timeout.
    """
    for attempt in range(max_retries):
        try:
            with urllib.request.urlopen(url, timeout=1) as resp:
                # If server returns 5xx, urlopen raises HTTPError before this point
                return resp.read()
        except urllib.error.URLError as e:
            # Only retry for HTTP 5xx if HTTPError
            if isinstance(e, urllib.error.HTTPError) and (e.code < 500 or e.code >= 600):
                raise
            if attempt == max_retries - 1:
                raise
            time.sleep(delay)
    raise RuntimeError("unreachable")


def test_retry_helper_succeeds_after_transient_failures():
    """
    Route fails with 500 twice, then succeeds; retry helper should succeed.
    """
    port = get_free_port()
    server = HTTPServerComponent(host="127.0.0.1", port=port)

    attempts = {"count": 0}

    @server.route("/flaky", method="GET")
    def flaky_handler(_req):
        attempts["count"] += 1
        # Raise to trigger server's exception handling -> 500
        if attempts["count"] < 3:
            raise RuntimeError("transient failure")
        return {"ok": True, "attempts": attempts["count"]}

    server.start()
    try:
        time.sleep(0.1)
        body = _retry_get(f"http://127.0.0.1:{port}/flaky", max_retries=5, delay=0.02)
        assert b"ok" in body
        assert attempts["count"] >= 3
    finally:
        server.stop()


def test_retry_helper_gives_up_with_low_max_retries():
    """
    With max_retries too low, helper should raise after exhausting attempts.
    """
    port = get_free_port()
    server = HTTPServerComponent(host="127.0.0.1", port=port)

    attempts = {"count": 0}

    @server.route("/always-fail", method="GET")
    def always_fail(_req):
        attempts["count"] += 1
        raise RuntimeError("still failing")

    server.start()
    try:
        time.sleep(0.1)
        raised = False
        try:
            _ = _retry_get(f"http://127.0.0.1:{port}/always-fail", max_retries=2, delay=0.01)
        except urllib.error.URLError:
            raised = True
        assert raised, "Expected the retry helper to raise"
        assert attempts["count"] >= 2
    finally:
        server.stop()
