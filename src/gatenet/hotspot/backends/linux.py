import subprocess
from typing import List, Dict
from ..backend import HotspotBackend, BackendResult

class LinuxBackend(HotspotBackend):
    def __init__(self, interface: str, gateway: str, ip_cidr: str, hostapd_conf: str):
        self.interface = interface
        self.gateway = gateway
        self.ip_cidr = ip_cidr
        self.hostapd_conf = hostapd_conf

    def start(self) -> BackendResult:
        try:
            with open("/tmp/hostapd.conf", "w") as f:
                f.write(self.hostapd_conf)
            subprocess.run(["sudo", "ip", "addr", "add", f"{self.gateway}/24", "dev", self.interface], check=False)
            subprocess.run(["sudo", "ip", "link", "set", self.interface, "up"], check=False)
            result = subprocess.run(["sudo", "hostapd", "/tmp/hostapd.conf"], capture_output=True, text=True, check=False)
            ok = result.returncode == 0
            return BackendResult(ok=ok, message=result.stderr.strip() if not ok else "")
        except Exception as e:
            return BackendResult(ok=False, message=str(e))

    def stop(self) -> BackendResult:
        try:
            subprocess.run(["sudo", "pkill", "hostapd"], check=False)
            subprocess.run(["sudo", "ip", "link", "set", self.interface, "down"], check=False)
            subprocess.run(["sudo", "ip", "addr", "flush", "dev", self.interface], check=False)
            return BackendResult(ok=True)
        except Exception as e:
            return BackendResult(ok=False, message=str(e))

    def devices(self) -> List[Dict[str, str]]:
        devices: List[Dict[str, str]] = []
        try:
            result = subprocess.run(["arp", "-a"], capture_output=True, text=True, check=False)
            for line in result.stdout.split('\n'):
                parts = line.split()
                if len(parts) >= 4:
                    hostname = parts[0]
                    ip = parts[1].strip('()')
                    mac = parts[3]
                    devices.append({"hostname": hostname, "ip": ip, "mac": mac})
        except Exception:
            pass
        return devices
