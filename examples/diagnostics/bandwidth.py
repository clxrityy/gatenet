from gatenet.diagnostics.bandwidth import measure_bandwidth

# Example: Bandwidth measurement using gatenet's measure_bandwidth
#
# This requires a simple custom bandwidth server, not iperf3.
#
# To test, first run this server in a separate terminal:
#
#     import socket
#     def bandwidth_server(host='0.0.0.0', port=5201, payload_size=65536):
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.bind((host, port))
#         s.listen(1)
#         print(f"Bandwidth server listening on {host}:{port}")
#         while True:
#             conn, addr = s.accept()
#             print(f"Connection from {addr}")
#             try:
#                 while True:
#                     conn.sendall(b'0' * payload_size)
#             except Exception:
#                 pass
#             finally:
#                 conn.close()
#     if __name__ == '__main__':
#         bandwidth_server()
#
# Then run this client example:

# Measure download bandwidth from the custom server
result = measure_bandwidth('127.0.0.1', port=5201, duration=3.0, direction='download')
print("Download:", result)

# Measure upload bandwidth (server just needs to accept and discard data)
result = measure_bandwidth('127.0.0.1', port=5201, duration=3.0, direction='upload')
print("Upload:", result)