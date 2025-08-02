CLI Usage
========

Gatenet provides a powerful, modular command-line interface (CLI) for diagnostics, service discovery, and network utilities. The CLI is designed for extensibility, colorized output, robust error handling, and highly configurable output and behavior via command-line arguments.

Overview
--------

The CLI is available as the `gatenet` command after installation:

.. code-block:: bash

   gatenet --help

This will display a colorized help message with all available commands and options, including global and command-specific arguments for output format, color, verbosity, and more.

Available Commands
------------------


- **iface**: List network interfaces and their details. Supports `--output-format`, `--color`, `--verbosity`, and `--default` to select the default interface.
- **wifi**: Scan for available WiFi networks (SSID, signal, security). Supports `--output-format`, `--color`, `--verbosity`, and `--interface` to select the WiFi adapter.
- **ping**: Send ICMP echo requests to a host (sync/async). Supports `--output-format`, `--color`, `--verbosity`, and `--count` for number of pings.
- **trace**: Perform a traceroute to a host. Supports `--output-format`, `--color`, `--verbosity`, and `--max-hops` for hop limit.
- **dns**: Perform DNS lookups and reverse lookups. Supports `--output-format`, `--color`, `--verbosity`, and `--server` for custom DNS server.
- **ports**: Scan TCP/UDP ports on a host. Supports `--output-format`, `--color`, `--verbosity`, and `--ports` for port selection.

Each command supports `--help` for detailed usage and options:

.. code-block:: bash

   gatenet iface --help
   gatenet wifi --help
   gatenet ping --help
   gatenet trace --help
   gatenet dns --help
   gatenet ports --help

All commands support the following global arguments:

- `--output-format [table|plain|json]`: Select output style (default: table)
- `--color [true|false]`: Enable or disable colorized output (default: true)
- `--verbosity [0|1|debug|info]`: Control verbosity level (default: 1)

Command-specific arguments:

- `iface`: `--default [iface_name]` to show a specific interface first
- `wifi`: `--interface [adapter]` to select WiFi adapter
- `ping`: `--count [N]` to set number of pings
- `trace`: `--max-hops [N]` to set hop limit
- `dns`: `--server [address]` to use a custom DNS server
- `ports`: `--ports [list]` to specify ports to scan

Example Usages
--------------


List network interfaces (table output, color):

.. code-block:: bash

   gatenet iface --output-format table --color true

Scan WiFi networks (plain output, no color):

.. code-block:: bash

   gatenet wifi --output-format plain --color false

Ping a host (JSON output, 4 pings):

.. code-block:: bash

   gatenet ping 8.8.8.8 --count 4 --output-format json

Traceroute (max 20 hops):

.. code-block:: bash

   gatenet trace google.com --max-hops 20

DNS lookup (custom DNS server):

.. code-block:: bash

   gatenet dns google.com --server 1.1.1.1

Port scan (scan specific ports):

.. code-block:: bash

   gatenet ports 127.0.0.1 --ports 22,80,443 --output-format plain

Features
--------


- Colorized, user-friendly output (using Rich)
- Robust error handling and clear error messages
- Configurable output formats: table, plain, JSON
- Verbosity control for debug/info output
- Modular command structure for easy extension
- All commands use only internal gatenet modules
- Command-specific options for advanced usage

For more details, see the API Reference and command module documentation.
