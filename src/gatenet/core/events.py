"""Common event names used across modules.

These constants help avoid typos and keep a shared vocabulary for hooks.
"""

# HTTP events
HTTP_BEFORE_REQUEST = "http:before_request"        # kwargs: req
HTTP_AFTER_RESPONSE = "http:after_response"        # kwargs: req, status, headers, body
HTTP_ROUTE_NOT_FOUND = "http:route_not_found"      # kwargs: path, method
HTTP_EXCEPTION = "http:exception"                  # kwargs: req, exc

# Client events
TCP_BEFORE_SEND = "tcp:before_send"                # kwargs: data
TCP_AFTER_RECV = "tcp:after_recv"                  # kwargs: data
UDP_BEFORE_SEND = "udp:before_send"                # kwargs: data
UDP_AFTER_RECV = "udp:after_recv"                  # kwargs: data

# Discovery events
DISCOVERY_BEFORE_DETECT = "discovery:before_detect"  # kwargs: port, banner
DISCOVERY_AFTER_DETECT = "discovery:after_detect"    # kwargs: port, banner, result

# Diagnostics events
PING_BEFORE = "diagnostics:ping:before"             # kwargs: host, count
PING_AFTER = "diagnostics:ping:after"               # kwargs: host, result
