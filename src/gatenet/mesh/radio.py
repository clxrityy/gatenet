import time
from typing import List, Dict

class MeshRadio:
    def on_signal(self, handler):
        """
        Register a signal handler (no-op for MeshRadio, for diagnostics integration compatibility).
        """
        # MeshRadio does not emit RF events, so this is a no-op
        pass
    def sync_logs(self, file_path: str = "mesh_radio_logs.json") -> bool:
        """
        Sync mesh radio logs (packets, topology, GPS, RF, Wi-Fi) to a file (base node or Mini PC).

        Args:
            file_path (str): Path to save logs (default: mesh_radio_logs.json)

        Returns:
            bool: True if successful, False otherwise

        Example:
            >>> radio = MeshRadio()
            >>> radio.sync_logs()
            >>> radio.sync_logs("/mnt/base_node/mesh_radio_logs.json")
        """
        import json
        try:
            logs = {
                "packets": self.packets,
                "topology": self.topology,
                "gps_location": self.gps_location,
                "rf_signal": self.rf_signal,
                "wifi_networks": self.wifi_networks
            }
            with open(file_path, "w") as f:
                json.dump(logs, f, indent=2)
            return True
        except Exception as e:
            print(f"Error syncing logs: {e}")
            return False
    """
    MeshRadio base class for mesh packet parsing, encrypted messaging, and topology mapping.

    Example:
        >>> from gatenet.mesh.radio import MeshRadio
        >>> radio = MeshRadio()
        >>> radio.log_gps(37.7749, -122.4194)
        >>> radio.log_rf_signal(-55.0)
        >>> radio.scan_wifi(mock=True)
        >>> radio.send_message("Hello", "node2")
        >>> packets = radio.receive_packets()
        >>> topology = radio.get_topology()
    """
    def __init__(self):
        self.topology = {
            "nodes": [], "links": [], "locations": [], "signals": [], "wifi": []
        }
        self.packets = []
        self.gps_location = None
        self.rf_signal = None
        self.wifi_networks = []

    def scan_wifi(self, interface: str = "wlan0", mock: bool = False):
        """
        Scan for Wi-Fi SSIDs/devices and correlate with mesh activity.
        On Raspberry Pi, uses 'iwlist' for real scan. If mock=True, returns sample data.

        Example:
            >>> radio = MeshRadio()
            >>> radio.scan_wifi(mock=True)
        """
        if mock:
            networks = [
                {"ssid": "TestNet", "mac": "AA:BB:CC:DD:EE:FF", "signal": -40},
                {"ssid": "HomeWiFi", "mac": "11:22:33:44:55:66", "signal": -60}
            ]
        else:
            import subprocess, re
            try:
                output = subprocess.check_output(["sudo", "iwlist", interface, "scan"], text=True)
                ssid_re = re.compile(r'ESSID:"([^"]+)"')
                mac_re = re.compile(r'Address: ([0-9A-Fa-f:]+)')
                signal_re = re.compile(r'Signal level=(-?\d+)')
                networks = []
                for cell in output.split("Cell ")[1:]:
                    ssid = ssid_re.search(cell)
                    mac = mac_re.search(cell)
                    signal = signal_re.search(cell)
                    networks.append({
                        "ssid": ssid.group(1) if ssid else None,
                        "mac": mac.group(1) if mac else None,
                        "signal": int(signal.group(1)) if signal else None
                    })
            except Exception as e:
                networks = [{"ssid": None, "mac": None, "signal": None, "error": str(e)}]
        self.wifi_networks = networks
        self.topology["wifi"] = networks
        return networks

    def log_gps(self, lat: float, lon: float):
        """
        Log GPS location for the mesh node.

        Example:
            >>> radio = MeshRadio()
            >>> radio.log_gps(37.7749, -122.4194)
        """
        self.gps_location = (lat, lon)
        self.topology["locations"].append({"node": "self", "lat": lat, "lon": lon})

    def log_rf_signal(self, signal_info):
        """
        Log RF signal info (strength, freq, type, etc) and propagate as mesh event.

        Args:
            signal_info (float or dict): RF info (can be just strength or full dict)

        Example:
            >>> radio = MeshRadio()
            >>> radio.log_rf_signal({"freq": 868000000, "power": 24, "type": "lora"})
        """
        self.rf_signal = signal_info
        self.topology["signals"].append({"node": "self", "signal": signal_info})
        handler = getattr(self, "on_rf_event", None)
        if callable(handler):
            handler(signal_info)

    def send_message(self, msg: str, dest: str, rf_signal=None) -> bool:
        """
        Send encrypted message to mesh node, optionally attaching RF signal info.

        Args:
            msg (str): Message to send
            dest (str): Destination node
            rf_signal (optional): RF info from radio module

        Example:
            >>> radio.send_message("alert", "node2", rf_signal={"freq": 868000000})
        """
        packet = {
            "src": "self",
            "dest": dest,
            "msg": self._encrypt(msg),
            "timestamp": time.time(),
            "gps": self.gps_location,
            "rf_signal": rf_signal if rf_signal is not None else self.rf_signal
        }
        self.packets.append(packet)
        self._update_topology(dest)
        return True

    def receive_packets(self) -> List[Dict]:
        """
        Receive and decrypt all packets sent by this node.

        Example:
            >>> radio = MeshRadio()
            >>> packets = radio.receive_packets()
        """
        return [self._decrypt_packet(pkt) for pkt in self.packets]

    def get_topology(self) -> Dict:
        """
        Get the current mesh topology (nodes, links, locations, signals, wifi).

        Example:
            >>> radio = MeshRadio()
            >>> topology = radio.get_topology()
        """
        return self.topology

    def _encrypt(self, msg: str) -> str:
        return f"enc({msg})"

    def _decrypt_packet(self, pkt: Dict) -> Dict:
        pkt = pkt.copy()
        pkt["msg"] = pkt["msg"].replace("enc(", "").replace(")", "")
        return pkt

    def _update_topology(self, dest: str):
        if dest not in self.topology["nodes"]:
            self.topology["nodes"].append(dest)
        self.topology["links"].append({"src": "self", "dest": dest})

