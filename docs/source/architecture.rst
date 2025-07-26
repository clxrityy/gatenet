.. _architecture:

Gatenet Architecture
====================

.. mermaid::

   mindmap
     root(🛰️)
       diagnostics/
         dns
         geo
         ping
         port_scan
         bandwidth
       client/
         base
           TCP
           UDP
       http_/
           base
               client
               server
               async_client
       socket/
           base
               TCP
               UDP
       discovery/
           MDNS
           UPNP
           SSH
           bluetooth

This mindmap shows the high-level structure of the Gatenet toolkit. Each module is modular, extensible, and well-tested.
