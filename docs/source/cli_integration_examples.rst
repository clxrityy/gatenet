CLI Integration Examples
=======================

This page shows how to use Gatenet's mesh hardware features from the command line, including Wi-Fi scanning, GPS logging, and RF signal tracking.

Wi-Fi Scan (Raspberry Pi)
------------------------

.. code-block:: bash

   # Scan Wi-Fi networks and correlate with mesh
   python3 -c "from gatenet.mesh import MeshRadio; mesh=MeshRadio(); print(mesh.scan_wifi(interface='wlan0'))"

   # Save results to a file
   python3 -c "from gatenet.mesh import MeshRadio; mesh=MeshRadio(); networks=mesh.scan_wifi(interface='wlan0'); import json; open('wifi_scan.json','w').write(json.dumps(networks, indent=2))"

GPS Logging
-----------

.. code-block:: bash

   # Log GPS location (example coordinates)
   python3 -c "from gatenet.mesh import MeshRadio; mesh=MeshRadio(); mesh.log_gps(37.7749, -122.4194); mesh.send_message('Hello', dest='node2'); print(mesh.packets[-1])"

   # Integrate with gpsd (requires python3-gps)
   python3 -c "import gps; from gatenet.mesh import MeshRadio; mesh=MeshRadio(); session=gps.gps(mode=gps.WATCH_ENABLE); report=next(session); mesh.log_gps(report.lat, report.lon); mesh.send_message('Hi', dest='node2'); print(mesh.packets[-1])"

RF Signal Logging
-----------------

.. code-block:: bash

   # Log RF signal strength
   python3 -c "from gatenet.mesh import MeshRadio; mesh=MeshRadio(); mesh.log_rf_signal(-65.0); mesh.send_message('Signal', dest='node3'); print(mesh.packets[-1])"

SDR Frequency Scan
------------------

.. code-block:: bash

   # Scan frequencies with RTL-SDR (requires pyrtlsdr)
   python3 -c "from rtlsdr import RtlSdr; from gatenet.mesh import MeshRadio; mesh=MeshRadio(); sdr=RtlSdr(); sdr.center_freq=100e6; sdr.sample_rate=2.048e6; sdr.gain='auto'; samples=sdr.read_samples(256*1024); # Analyze samples for activity; mesh.log_rf_signal(-50.0); mesh.send_message('SDR', dest='node4'); print(mesh.packets[-1])"

See the hardware_setup docs for more details and troubleshooting.
