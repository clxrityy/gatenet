"""
Example: Launch the Gatenet dashboard UI and API.
"""
from gatenet.dashboard import launch_dashboard

if __name__ == "__main__":
    launch_dashboard(host="127.0.0.1", port=8000, open_browser=True)
