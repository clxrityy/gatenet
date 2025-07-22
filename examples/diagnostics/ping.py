from gatenet.diagnostics.ping import ping, async_ping
import asyncio

# Synchronous ICMP ping
print("Synchronous ICMP ping to 1.1.1.1:")
result = ping("1.1.1.1", count=3, method="icmp")
print(result)

# Synchronous TCP ping
print("\nSynchronous TCP ping to 1.1.1.1:")
result = ping("1.1.1.1", count=3, method="tcp")
print(result)

# Asynchronous ICMP ping
async def run_async_icmp():
    print("\nAsynchronous ICMP ping to 8.8.8.8:")
    result = await async_ping("8.8.8.8", count=3, method="icmp")
    print(result)

# Asynchronous TCP ping
async def run_async_tcp():
    print("\nAsynchronous TCP ping to 8.8.8.8:")
    result = await async_ping("8.8.8.8", count=3, method="tcp")
    print(result)

if __name__ == "__main__":
    asyncio.run(run_async_icmp())
    asyncio.run(run_async_tcp())
