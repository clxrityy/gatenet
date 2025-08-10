import time
import urllib.request
from typing import List, Tuple

from gatenet.core import Hooks, events
from gatenet.http_.server import HTTPServerComponent
from gatenet.utils import get_free_port


def test_http_hooks_emit_on_request():
    hooks = Hooks()

    before: List[str] = []
    after: List[Tuple[int, str]] = []

    hooks.on(events.HTTP_BEFORE_REQUEST, lambda req: before.append(getattr(req, "path", "")))
    hooks.on(
        events.HTTP_AFTER_RESPONSE,
        lambda req, status, headers, body: after.append((status, getattr(req, "path", ""))),
    )

    port = get_free_port()
    server = HTTPServerComponent(host="127.0.0.1", port=port, hooks=hooks)

    @server.route("/status", method="GET")
    def status_handler(_req):
        return {"ok": True}

    server.start()
    try:
        time.sleep(0.1)
        url = f"http://127.0.0.1:{port}/status"
        with urllib.request.urlopen(url, timeout=2) as resp:
            assert resp.status == 200
            data = resp.read()
            assert b"ok" in data
    finally:
        server.stop()

    # Verify hooks captured the request and response
    assert "/status" in before
    assert any(status == 200 and path == "/status" for status, path in after)
