Advanced Radio Usage
===================

This page covers advanced features and workflows for radio integration in Gatenet, including protocol decoding, spectrogram visualization, RF fingerprinting, and hardware compatibility.

Protocol Decoding
-----------------

**ADS-B Aircraft Messages**

.. code-block:: python

   from gatenet.radio import SDRRadio
   radio = SDRRadio()
   aircraft = radio.decode_adsb()
   for plane in aircraft:
       print(plane)

**Weather Station Signals**

.. code-block:: python

   from gatenet.radio import SDRRadio
   weather = radio.decode_weather()
   print(weather)

Spectrogram Visualization
------------------------

Visualize RF activity in real time using matplotlib or OpenGL:

.. code-block:: python

   import matplotlib.pyplot as plt
   from gatenet.radio import SDRRadio
   radio = SDRRadio()
   samples = radio.get_samples()
   plt.specgram(samples, NFFT=1024, Fs=radio.sample_rate)
   plt.show()

RF Fingerprinting & ML
----------------------

Extract unique features from RF signals for device identification:

.. code-block:: python

   from gatenet.radio import SDRRadio
   import numpy as np
   radio = SDRRadio()
   samples = radio.get_samples()
   fft = np.fft.fft(samples)
   # Use ML model to classify/fingerprint
   # model.predict(fft)

Collision Detection
------------------

Detect and handle RF collisions between sources:

.. code-block:: python

   from gatenet.radio import SDRRadio
   radio = SDRRadio()
   collisions = radio.detect_collisions()
   print(collisions)

Hardware Compatibility
----------------------

Supported devices:
- RTL-SDR USB dongle
- LoRa modules (e.g., SX127x)
- ESP32/ESP8266
- Weather station receivers

Refer to the Hardware Setup page for installation and driver details.

Auto-Switch Scanning by GPS
---------------------------

Change scanning presets based on location:

.. code-block:: python

   from gatenet.radio import SDRRadio
   radio = SDRRadio()
   gps = radio.get_gps()
   if gps['lat'] > 40.0:
       radio.scan_frequencies(433_000_000, 434_000_000, 10)
   else:
       radio.scan_frequencies(868_000_000, 869_000_000, 125)

See also: Hardware Setup, CLI Integration Examples, and API Reference for more details.

Log Syncing & Archival
---------------------

Save mesh radio logs (packets, topology, GPS, RF, Wi-Fi) to a file for base node or Mini PC integration:

.. code-block:: python

   from gatenet.mesh.radio import MeshRadio
   radio = MeshRadio()
   # ... collect data ...
   radio.sync_logs()  # Saves to mesh_radio_logs.json
   radio.sync_logs("/mnt/base_node/mesh_radio_logs.json")  # Custom path

The log file contains all mesh packets, topology, GPS, RF, and Wi-Fi data for later analysis or backup.
