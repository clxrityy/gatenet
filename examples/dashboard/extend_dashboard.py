"""
Example: Extend the Gatenet dashboard FastAPI app with a custom endpoint.
"""
from gatenet.dashboard.app import app
from gatenet.dashboard import launch_dashboard

@app.get("/api/hello")
def hello():
    return {"message": "Hello from custom endpoint!"}

if __name__ == "__main__":
    launch_dashboard()
