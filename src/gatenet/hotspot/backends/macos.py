import subprocess
from typing import List, Dict
from ..backend import HotspotBackend, BackendResult

class MacOSBackend(HotspotBackend):
    def start(self) -> BackendResult:
        try:
            subprocess.run(["sudo", "launchctl", "load", "-w",
                            "/System/Library/LaunchDaemons/com.apple.InternetSharing.plist"],
                           check=False)
            return BackendResult(ok=True)
        except Exception as e:
            return BackendResult(ok=False, message=str(e))

    def stop(self) -> BackendResult:
        try:
            subprocess.run(["sudo", "launchctl", "unload", "-w",
                            "/System/Library/LaunchDaemons/com.apple.InternetSharing.plist"],
                           check=False)
            return BackendResult(ok=True)
        except Exception as e:
            return BackendResult(ok=False, message=str(e))

    def devices(self) -> List[Dict[str, str]]:
        # Fallback to ARP list for now
        try:
            result = subprocess.run(["arp", "-a"], capture_output=True, text=True, check=False)
            devices = []
            for line in result.stdout.split('\n'):
                parts = line.split()
                if len(parts) >= 4:
                    hostname = parts[0]
                    ip = parts[1].strip('()')
                    mac = parts[3]
                    devices.append({"hostname": hostname, "ip": ip, "mac": mac})
            return devices
        except Exception:
            return []
