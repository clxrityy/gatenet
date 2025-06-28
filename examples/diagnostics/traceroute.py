from gatenet.diagnostics.traceroute import traceroute

hops = traceroute("google.com")
for hop in hops:
    print(hop)