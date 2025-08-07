.. _sandbox:

Interactive Sandbox
====================

Welcome to the Gatenet Interactive Sandbox! Here you can try out Gatenet features directly in your browser without installing anything.

.. note::
   The sandbox provides a safe environment to experiment with Gatenet's networking tools. Some features may be limited in the browser environment.

Live Dashboard
--------------

The Gatenet dashboard provides an interactive web interface for network diagnostics:

.. raw:: html

   <div class="sandbox-container">
     <h3>🚀 Gatenet Live Dashboard</h3>
     <p>Experience the full Gatenet dashboard with ping, traceroute, DNS lookup, and port scanning tools.</p>
     <div class="dashboard-embed">
       <iframe src="https://gatenet-demo-c27e0a76554d.herokuapp.com/" width="100%" height="600" frameborder="0" style="border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"></iframe>
       <p style="margin-top: 10px; font-size: 0.9em; color: #666;">
         <em>Note: This is a demo instance. For full functionality, install Gatenet locally.</em>
       </p>
     </div>
   </div>

Interactive Code Examples
--------------------------

Try these code examples directly in your browser:

.. raw:: html

   <div class="code-sandbox">
     <h3>📦 HTTP Client Example</h3>
     <div class="code-editor" id="http-example">
       <textarea id="http-code" rows="15" cols="80">
   # HTTP Client Example - Try it out!
   from gatenet.http_.client import HTTPClient

   # Create a client
   client = HTTPClient("https://httpbin.org")

   # Make a GET request
   response = client.get("/json")
   print("GET Response:", response["data"])

   # Make a POST request
   payload = {"message": "Hello from Gatenet!", "user": "sandbox"}
   post_response = client.post("/post", data=payload)
   print("POST Response:", post_response["data"]["json"])
       </textarea>
       <div class="code-actions">
         <button onclick="runHttpExample()" class="run-button">▶ Run Code</button>
         <button onclick="resetHttpExample()" class="reset-button">🔄 Reset</button>
       </div>
       <div class="code-output">
         <h4>Output:</h4>
         <pre id="http-output">Click "Run Code" to see the output...</pre>
       </div>
     </div>
   </div>

   <div class="code-sandbox">
     <h3>🔍 Network Diagnostics Example</h3>
     <div class="code-editor" id="diagnostics-example">
       <textarea id="diagnostics-code" rows="15" cols="80">
   # Network Diagnostics Example
   from gatenet.diagnostics.dns import dns_lookup
   from gatenet.diagnostics.geo import get_geo_info
   from gatenet.diagnostics.ping import ping

   # DNS Lookup
   ip = dns_lookup("google.com")
   print(f"google.com resolves to: {ip}")

   # Geo IP Information
   geo = get_geo_info("8.8.8.8")
   print(f"8.8.8.8 location: {geo}")

   # Ping test (simulated in browser)
   result = ping("1.1.1.1", count=3)
   print(f"Ping result: {result}")
       </textarea>
       <div class="code-actions">
         <button onclick="runDiagnosticsExample()" class="run-button">▶ Run Code</button>
         <button onclick="resetDiagnosticsExample()" class="reset-button">🔄 Reset</button>
       </div>
       <div class="code-output">
         <h4>Output:</h4>
         <pre id="diagnostics-output">Click "Run Code" to see the output...</pre>
       </div>
     </div>
   </div>

   <div class="code-sandbox">
     <h3>🕵️ Service Discovery Example</h3>
     <div class="code-editor" id="discovery-example">
       <textarea id="discovery-code" rows="15" cols="80">
   # Service Discovery Example
   from gatenet.discovery.ssh import _identify_service, SSHDetector

   # Basic service identification
   service = _identify_service(22, "SSH-2.0-OpenSSH_8.9p1")
   print(f"Port 22 service: {service}")

   # HTTP service detection
   http_service = _identify_service(80, "Server: nginx/1.18.0")
   print(f"Port 80 service: {http_service}")

   # Using individual detectors
   ssh_detector = SSHDetector()
   result = ssh_detector.detect(22, "SSH-2.0-OpenSSH_8.9p1")
   print(f"SSH detector result: {result}")

   # Multiple service tests
   services = [
       (443, ""),  # HTTPS
       (25, "220 Postfix SMTP"),
       (3306, "MySQL Server 8.0.25")
   ]

   for port, banner in services:
       identified = _identify_service(port, banner)
       print(f"Port {port}: {identified}")
       </textarea>
       <div class="code-actions">
         <button onclick="runDiscoveryExample()" class="run-button">▶ Run Code</button>
         <button onclick="resetDiscoveryExample()" class="reset-button">🔄 Reset</button>
       </div>
       <div class="code-output">
         <h4>Output:</h4>
         <pre id="discovery-output">Click "Run Code" to see the output...</pre>
       </div>
     </div>
   </div>

Quick Start Playground
-----------------------

.. raw:: html

   <div class="playground-container">
     <h3>🎮 Quick Start Playground</h3>
     <p>Try common Gatenet operations with pre-configured examples:</p>
     
     <div class="playground-grid">
       <div class="playground-card">
         <h4>🌐 HTTP Request</h4>
         <button onclick="quickHttpTest()" class="playground-button">Test HTTP Client</button>
         <div id="quick-http-result" class="playground-result"></div>
       </div>
       
       <div class="playground-card">
         <h4>🔍 DNS Lookup</h4>
         <input type="text" id="dns-input" placeholder="Enter domain (e.g., google.com)" value="google.com">
         <button onclick="quickDnsTest()" class="playground-button">Lookup DNS</button>
         <div id="quick-dns-result" class="playground-result"></div>
       </div>
       
       <div class="playground-card">
         <h4>📡 Service Detection</h4>
         <select id="service-select">
           <option value="22,SSH-2.0-OpenSSH_8.9p1">SSH Server</option>
           <option value="80,Server: nginx/1.18.0">Nginx Server</option>
           <option value="443,">HTTPS Server</option>
           <option value="25,220 Postfix SMTP">SMTP Server</option>
         </select>
         <button onclick="quickServiceTest()" class="playground-button">Identify Service</button>
         <div id="quick-service-result" class="playground-result"></div>
       </div>
       
       <div class="playground-card">
         <h4>🌍 Geo IP Lookup</h4>
         <input type="text" id="ip-input" placeholder="Enter IP (e.g., 8.8.8.8)" value="8.8.8.8">
         <button onclick="quickGeoTest()" class="playground-button">Get Location</button>
         <div id="quick-geo-result" class="playground-result"></div>
       </div>
     </div>
   </div>

Local Development
-----------------

To run your own Gatenet sandbox locally:

.. code-block:: bash

   # Install Gatenet
   pip install gatenet

   # Launch the dashboard
   python -c "from gatenet.dashboard import launch_dashboard; launch_dashboard()"

   # Or create a custom sandbox
   python -c "
   from gatenet.dashboard.app import app
   from gatenet.dashboard import launch_dashboard

   @app.get('/api/sandbox')
   def sandbox():
       return {'message': 'Custom sandbox endpoint!'}

   launch_dashboard(host='127.0.0.1', port=8000)
   "

Try the Examples Locally
-------------------------

All sandbox examples are available as runnable scripts in the `examples/` directory:

.. code-block:: bash

   git clone https://github.com/clxrityy/gatenet.git
   cd gatenet/examples
   
   # HTTP examples
   python http_/http_example.py
   python http_/async_client_usage.py
   
   # Diagnostics examples
   python diagnostics/dns_lookup.py
   python diagnostics/port_scanning.py
   
   # Discovery examples
   python discovery/ssh_discovery.py
   
   # Dashboard examples
   python dashboard/launch_dashboard.py

.. note::
   **Security Note**: The sandbox environment simulates network operations for demonstration purposes. Real network operations require appropriate permissions and may be restricted in browser environments.
