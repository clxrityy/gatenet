from gatenet.discovery.upnp import discover_upnp_devices

devices = discover_upnp_devices()
for device in devices:
    print(device.get("SERVER"), device.get("LOCATION"))

# Example output:
# Linux UPnP/1.0 Gateway/1.0 (UPnP-1.0) UPnP/1.0 Gateway/1.0
# http://192.168.1.1:80/rootDesc.xml
# Note: The output will depend on the devices available on your network.
# Make sure to run this script in an environment where UPnP devices are present.