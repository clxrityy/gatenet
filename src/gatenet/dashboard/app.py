"""
FastAPI-based dashboard app for Gatenet.

Provides diagnostics, service discovery, and monitoring endpoints and UI.
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse


from gatenet.diagnostics.ping import ping
from gatenet.diagnostics.traceroute import traceroute
from gatenet.diagnostics.dns import dns_lookup
from gatenet.diagnostics.port_scan import scan_ports
from fastapi.responses import StreamingResponse
import time
from fastapi import Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Gatenet Dashboard", docs_url="/docs")

error_message = "An internal error occurred. Please try again later."

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <html>
        <head>
            <title>Gatenet Dashboard</title>
            <script>
            async function doPing() {
                const host = document.getElementById('ping_host').value;
                const res = await fetch(`/api/ping?host=${encodeURIComponent(host)}`);
                const data = await res.json();
                document.getElementById('ping_result').textContent = JSON.stringify(data, null, 2);
            }
            async function doTraceroute() {
                const host = document.getElementById('tr_host').value;
                const res = await fetch(`/api/traceroute?host=${encodeURIComponent(host)}`);
                const data = await res.json();
                document.getElementById('tr_result').textContent = JSON.stringify(data, null, 2);
            }
            function doLiveTraceroute() {
                const host = document.getElementById('tr_host').value;
                const eventSource = new EventSource(`/api/traceroute/stream?host=${encodeURIComponent(host)}`);
                let output = '';
                eventSource.onmessage = function(event) {
                    output += event.data + '\n';
                    document.getElementById('tr_live_result').textContent = output;
                };
                eventSource.onerror = function() {
                    eventSource.close();
                };
            }
            async function doDNSLookup() {
                const host = document.getElementById('dns_host').value;
                const res = await fetch(`/api/dns_lookup?host=${encodeURIComponent(host)}`);
                const data = await res.json();
                document.getElementById('dns_result').textContent = JSON.stringify(data, null, 2);
            }
            async function doPortScan() {
                const host = document.getElementById('ps_host').value;
                const ports = document.getElementById('ps_ports').value;
                const res = await fetch(`/api/port_scan?host=${encodeURIComponent(host)}&ports=${encodeURIComponent(ports)}`);
                const data = await res.json();
                document.getElementById('ps_result').textContent = JSON.stringify(data, null, 2);
            }
            </script>
        </head>
        <body>
            <h1>Gatenet Dashboard</h1>
            <h2>Diagnostics</h2>
            <div>
                <h3>Ping</h3>
                <input id="ping_host" placeholder="Host (e.g. 8.8.8.8)" />
                <button onclick="doPing()">Ping</button>
                <pre id="ping_result"></pre>
            </div>
            <div>
                <h3>Traceroute</h3>
                <input id="tr_host" placeholder="Host (e.g. google.com)" />
                <button onclick="doTraceroute()">Traceroute</button>
                <pre id="tr_result"></pre>
            </div>
            <div>
                <h3>Live Traceroute (SSE)</h3>
                <button onclick="doLiveTraceroute()">Start Live Traceroute</button>
                <pre id="tr_live_result"></pre>
            </div>
            <div>
                <h3>DNS Lookup</h3>
                <input id="dns_host" placeholder="Host (e.g. google.com)" />
                <button onclick="doDNSLookup()">DNS Lookup</button>
                <pre id="dns_result"></pre>
            </div>
            <div>
                <h3>Port Scan</h3>
                <input id="ps_host" placeholder="Host (e.g. 127.0.0.1)" />
                <input id="ps_ports" placeholder="Ports (comma-separated, e.g. 22,80,443)" />
                <button onclick="doPortScan()">Scan Ports</button>
                <pre id="ps_result"></pre>
            </div>
        </body>
    </html>
    """

@app.get("/api/dns_lookup")
def api_dns_lookup(host: str = Query(..., description="Host to resolve")):
    """DNS lookup for a host."""
    try:
        ip = dns_lookup(host)
        return {"ok": True, "ip": ip}
    except Exception:
        # Log internally, but never expose details to user
        import logging
        logging.error("Error in api_dns_lookup")
        return {"ok": False, "error": error_message}


@app.get("/api/port_scan")
def api_port_scan(host: str = Query(..., description="Host to scan"), ports: str = Query(..., description="Comma-separated ports")):
    """Scan ports on a host."""
    try:
        port_list = [int(p.strip()) for p in ports.split(",") if p.strip().isdigit()]
        open_ports = scan_ports(host, ports=port_list)
        return {"ok": True, "open_ports": open_ports}
    except Exception:
        import logging
        logging.error("Error in api_port_scan")
        return {"ok": False, "error": error_message}


# SSE endpoint for live traceroute
@app.get("/api/traceroute/stream")
def api_traceroute_stream(host: str = Query(..., description="Host to traceroute")):
    """Stream traceroute hops as they are discovered (SSE)."""
    def event_stream():
        try:
            hops = traceroute(host)
            for hop in hops:
                yield f"data: {hop}\n\n"
                time.sleep(0.2)  # Simulate delay for demo
        except Exception:
            # Never leak exception details to SSE client
            yield "data: ERROR: An internal error occurred.\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.get("/api/ping")
def api_ping(host: str = Query(..., description="Host to ping"), count: int = Query(3, ge=1, le=10)):
    """Ping a host and return the result."""
    import logging
    try:
        result = ping(host, count=count)
        # If ping failed, never expose internal error details
        if not result.get("success", True):
            logging.error(f"Ping failed for host {host}: {result.get('error', '')}")
            return {"ok": False, "error": error_message}
        allowed_fields = ["host", "rtt_avg", "rtt_min", "rtt_max", "jitter", "packet_loss", "success", "sent", "received", "rtt_all"]
        sanitized_result = {k: v for k, v in result.items() if k in allowed_fields}
        # Only expose safe output fields, exclude raw_output, error, etc.
        return {"ok": True, "result": sanitized_result}
    except Exception:
        logging.error("Error in api_ping", exc_info=True)
        return {"ok": False, "error": error_message}
@app.get("/api/traceroute")
def api_traceroute(host: str = Query(..., description="Host to traceroute")):
    """Traceroute to a host and return hops."""
    try:
        hops = traceroute(host)
        return {"ok": True, "hops": hops}
    except Exception:
        import logging
        logging.error("Error in /api/traceroute endpoint")
        return {"ok": False, "error": error_message}

def launch_dashboard(host: str = "127.0.0.1", port: int = 8000, open_browser: bool = True) -> None:
    """
    Launch the Gatenet dashboard web app.
    
    Args:
        host (str): Host to bind the server to.
        port (int): Port to run the server on.
        open_browser (bool): Whether to open the dashboard in a browser.
    """
    import uvicorn
    import webbrowser
    if open_browser:
        webbrowser.open(f"http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)
