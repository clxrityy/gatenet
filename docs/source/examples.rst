.. _examples:

Examples
========

This section provides a reference to all Gatenet examples, organized by feature area. Each example demonstrates practical usage and is written directly in the documentation.

HTTP
----

**GET & POST requests**

.. code-block:: python

   from gatenet.http_.client import HTTPClient
   client = HTTPClient("http://localhost:8080")
   response = client.get("/status")
   print(response)
   response = client.post("/echo", data={"msg": "hello"})
   print(response)

**Timeout & retry**

.. code-block:: python

   from gatenet.http_.client import HTTPClient
   client = HTTPClient("http://localhost:8080", timeout=2, retries=3)
   try:
       response = client.get("/slow")
   except Exception as e:
       print("Request failed after retries:", e)

**Asynchronous Client**

.. code-block:: python

   from gatenet.http_.async_client import AsyncHTTPClient
   import asyncio
   async def main():
       client = AsyncHTTPClient("http://localhost:8080")
       response = await client.get("/status")
       print(response)
   asyncio.run(main())

TCP & UDP
---------

**With polymorphism**

.. code-block:: python

   from gatenet.client.tcp import TCPClient
   from gatenet.client.udp import UDPClient
   for Client in (TCPClient, UDPClient):
       client = Client(host="127.0.0.1", port=12345)
       client.connect()
       response = client.send("ping")
       print(response)
       client.close()

Diagnostics
-----------

**DNS Lookup**

.. code-block:: python

   from gatenet.diagnostics.dns import dns_lookup
   ip = dns_lookup("google.com")
   print(ip)

**Port Scanning**

.. code-block:: python

   from gatenet.diagnostics.port_scan import scan_ports
   open_ports = scan_ports("127.0.0.1", ports=[22, 80, 443])
   print(open_ports)

**Geo Information**

.. code-block:: python

   from gatenet.diagnostics.geo import get_geo_info
   geo = get_geo_info("8.8.8.8")
   print(geo)

**Traceroute**

.. code-block:: python

   from gatenet.diagnostics.traceroute import traceroute
   hops = traceroute("google.com")
   for hop in hops:
       print(hop)


**Bandwidth**

.. code-block:: python

   # This requires a custom bandwidth server (see gatenet example)
   from gatenet.diagnostics.bandwidth import measure_bandwidth
   result = measure_bandwidth("127.0.0.1", port=5201, duration=3.0, direction="download")
   print("Download:", result)
   result = measure_bandwidth("127.0.0.1", port=5201, duration=3.0, direction="upload")
   print("Upload:", result)

**Ping**

.. code-block:: python

   from gatenet.diagnostics.ping import ping
   result = ping("1.1.1.1", count=3)
   print(result)

Discovery
---------

**mDNS Discovery**

.. code-block:: python

   from gatenet.discovery.mdns import discover_mdns
   results = discover_mdns()
   print(results)

**SSDP Discovery**

.. code-block:: python

   from gatenet.discovery.ssdp import discover_ssdp
   results = discover_ssdp()
   print(results)


Dashboard
---------

**Launch the dashboard UI and API**

.. code-block:: python

   from gatenet.dashboard import launch_dashboard
   launch_dashboard(host="127.0.0.1", port=8000, open_browser=True)
   # Visit http://127.0.0.1:8000 in your browser

**Extend the dashboard FastAPI app**

.. code-block:: python

   from gatenet.dashboard.app import app
   from gatenet.dashboard import launch_dashboard

   @app.get("/api/hello")
   def hello():
       return {"message": "Hello from custom endpoint!"}

   if __name__ == "__main__":
       launch_dashboard()

**Bluetooth Discovery**

.. code-block:: python

   from gatenet.discovery.bluetooth import discover_bluetooth
   results = discover_bluetooth()
   print(results)

**SSH Discovery**

.. code-block:: python

   from gatenet.discovery.ssh import _identify_service, SSHDetector
   service = _identify_service(22, "SSH-2.0-OpenSSH_8.9p1")
   print(service)
   ssh_detector = SSHDetector()
   result = ssh_detector.detect(22, "ssh-2.0-openssh_8.9p1")
   print(result)

   # Custom detector example
   from gatenet.discovery.ssh import ServiceDetector
   from typing import Optional
   class CustomDetector(ServiceDetector):
       def detect(self, port: int, banner: str) -> Optional[str]:
           if 'myapp' in banner:
               return "MyCustomApp"
           return None
