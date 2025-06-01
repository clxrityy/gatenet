import platform
import subprocess
from typing import Optional, Dict

def ping(host: str, count: int = 4, timeout: int = 2) -> Dict[str, Optional[str]]:
    """
    Ping a host and return basic statistics.
    
    :param host: The hostname or IP address to ping.
    :param count: Number of echo requests to send.
    :param timeout: Timeout in seconds for each ping/request.
    :return: A dict with success status and summary output.
    """
    
    system = platform.system()
    
    if system == "Windows":
        cmd = ["ping", "-n", str(count), "-w", str(timeout * 1000), host]
    else:  # Assuming Unix-like systems
        cmd = ["ping", "-c", str(count), "-W", str(timeout), host]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return {
            "host": host,
            "success": result.returncode == 0,
            "output": result.stdout.strip(),
            "error": result.stderr.strip() if result.stderr else None
        }
        
    except Exception as e:
        return {
            "host": host,
            "success": False,
            "output": None,
            "error": str(e)
        }