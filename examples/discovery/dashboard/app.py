from flask import Flask, render_template
from gatenet.discovery.mdns import discover_mdns_services
from gatenet.discovery.upnp import discover_upnp_devices

app = Flask(__name__)


@app.route('/')
def index():
    """
    Render the main dashboard page with discovered devices.
    """
    mdns_services = discover_mdns_services(timeout=5)
    upnp_devices = discover_upnp_devices(timeout=5)

    return render_template('index.html', mdns=mdns_services, ssdp=upnp_devices)