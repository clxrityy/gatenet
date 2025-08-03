Hardware Setup
=============

.. toctree::
   :maxdepth: 2

   raspberry_pi_wifi
   gps_module
   sdr_radio


Raspberry Pi Wi-Fi Scanning
--------------------------

To enable Wi-Fi scanning and correlation with mesh activity on a Raspberry Pi:

1. Ensure you have a compatible Wi-Fi chip (e.g., built-in or USB dongle).
2. Install required tools:

   .. code-block:: bash

      sudo apt-get update
      sudo apt-get install wireless-tools

3. Enable the Wi-Fi interface (usually `wlan0`):

   .. code-block:: bash

      sudo ifconfig wlan0 up

4. Run mesh Wi-Fi scan in Python:

   .. code-block:: python

      from gatenet.mesh import MeshRadio
      mesh = MeshRadio()
      networks = mesh.scan_wifi(interface="wlan0")
      print(networks)

5. For non-root users, you may need to add permissions for `iwlist` or run with `sudo`.

GPS Module Integration
----------------------

To log GPS location with MeshRadio:

1. Connect a USB or serial GPS module (e.g., u-blox, Adafruit Ultimate GPS).
2. Install `gpsd` and Python bindings:

   .. code-block:: bash

      sudo apt-get install gpsd gpsd-clients python3-gps

3. Start the GPS daemon:

   .. code-block:: bash

      sudo systemctl start gpsd

4. Read GPS data in Python:

   .. code-block:: python

      import gps
      session = gps.gps(mode=gps.WATCH_ENABLE)
      report = next(session)
      lat, lon = report.lat, report.lon
      mesh.log_gps(lat, lon)

SDR Radio Integration
---------------------

To scan frequencies and map RF activity:

1. Connect an SDR device (e.g., RTL-SDR USB dongle).
2. Install SDR tools:

   .. code-block:: bash

      sudo apt-get install rtl-sdr
      pip install pyrtlsdr

3. Scan frequencies in Python:

   .. code-block:: python

      from rtlsdr import RtlSdr
      sdr = RtlSdr()
      sdr.center_freq = 100e6
      sdr.sample_rate = 2.048e6
      sdr.gain = 'auto'
      samples = sdr.read_samples(256*1024)
      # Analyze samples for activity, then mesh.log_rf_signal(signal_strength)

See each subpage for more details and troubleshooting.
