import asyncio
from gatenet.http_.async_client import AsyncHTTPClient

async def main():
    client = AsyncHTTPClient("http://127.0.0.1:8000")
    
    # Example of a GET request
    status = await client.get("/status")
    print("GET /status response:", status)
    
    # Example of a POST request
    payload = { "foo": "bar" }
    echo = await client.post("/echo", data=payload)
    print("POST /echo response:", echo)
    
if __name__ == "__main__":
    asyncio.run(main())
# This script demonstrates how to use the AsyncHTTPClient to make asynchronous HTTP requests.
# It includes examples of both GET and POST requests.
# Make sure to run an HTTP server at http://127.0.0.1:8000 that can handle the `/status` and `/echo` endpoints for testing.