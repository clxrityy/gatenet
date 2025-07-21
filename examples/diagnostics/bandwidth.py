from gatenet.diagnostics.bandwidth import measure_bandwidth

# Measure download bandwidth from a local iperf3 server
result = measure_bandwidth('127.0.0.1', port=5201, duration=3.0, direction='download')
print(result)
# Output: {'bandwidth_mbps': 123.45, 'bytes_transferred': 12345678, 'duration': 3.01}

# Measure upload bandwidth
result = measure_bandwidth('127.0.0.1', port=5201, duration=3.0, direction='upload')
print(result)