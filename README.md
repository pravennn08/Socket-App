<div align="center">

<h1>Socket App</h1>

<p>A Python desktop application for sending and receiving UDP text messages through a CustomTkinter interface.</p>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-1F6AA5?style=for-the-badge)
![Socket](https://img.shields.io/badge/Socket-Standard_Library-555555?style=for-the-badge)
![UDP](https://img.shields.io/badge/UDP-IPv4-008080?style=for-the-badge)

[Overview](#overview) • [Technology Stack](#technology-stack) • [Getting Started](#getting-started) • [Usage](#usage) • [Helper Methods](#helper-methods) • [Implementation Notes](#implementation-notes)

</div>

## Overview

Socket App explores basic network communication using Python's built-in `socket` library and a CustomTkinter desktop interface. Its `SocketHelper` class handles local IPv4 address lookup, outgoing text datagrams, and incoming messages with sender information.

The project demonstrates socket creation, address binding, text encoding, receive timeouts, and automatic socket cleanup. The networking behavior documented here follows the supplied helper code; GUI layout and control names depend on the application's interface implementation.

### Features

- **Local address lookup:** Obtain the local IPv4 address selected for a configured network destination.
- **UDP messaging:** Send text to a specified IPv4 address and port.
- **Message reception:** Receive a text message together with the sender's IP address and source port.
- **Bounded receive wait:** Wait up to one second for a datagram during each receive call.
- **Automatic cleanup:** Close temporary sockets when their context managers exit.
- **Desktop interface:** Use CustomTkinter as the application's GUI library.

## Technology Stack

| Technology    | Role                                                    |
| ------------- | ------------------------------------------------------- |
| Python        | Application logic and helper methods                    |
| CustomTkinter | Desktop graphical interface                             |
| `socket`      | IPv4 UDP communication using `AF_INET` and `SOCK_DGRAM` |

The `socket` module is included with Python and does not require a separate installation. Its address and socket operations are documented in the [Python socket reference](https://docs.python.org/3/library/socket.html).

## Getting Started

### Prerequisites

- Python 3 with Tkinter support.
- A desktop environment for the GUI.
- Two application instances or a compatible UDP peer on a reachable network.

### Install dependencies

From the project directory, create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Or on macOS/Linux:

```bash
source .venv/bin/activate
```

Install the GUI dependency:

```bash
python -m pip install customtkinter
```

If the repository provides a `requirements.txt`, use its dependency list instead:

```bash
python -m pip install -r requirements.txt
```

### Start the application

Run the Python file that creates the CustomTkinter window. For example, **if the GUI entry point is named `app.py`**:

```bash
python app.py
```

The GUI entry-point filename was not supplied; replace `app.py` with the actual filename in your repository.

## Usage

1. Connect the participating devices to a network that permits UDP communication between them.
2. Identify the receiving device's local IPv4 address and choose its listening port.
3. Start receiving on that device before sending a message. Each helper receive call listens for only one datagram, with a one-second timeout.
4. On the sending device, provide the receiver's IP address, listening port, and text message.
5. Read the received text and sender information returned by the helper.

For bidirectional messaging, each side must run its own receive operation and send to the other side's listening address and port.

### Network settings

| Setting                     | Value or behavior in the supplied code                   |
| --------------------------- | -------------------------------------------------------- |
| Address family              | IPv4                                                     |
| Transport                   | UDP                                                      |
| Local-IP lookup destination | `192.168.100.27:6000`                                    |
| Default receive address     | `self.local_ip`, captured during initialization          |
| Default receive port        | `6000` when both receive arguments are omitted           |
| Receive timeout             | 1 second                                                 |
| Receive buffer              | 1,024 bytes per call                                     |
| Text encoding               | UTF-8 through default `encode()` and `decode()` behavior |

The lookup destination is a hard-coded private network address. Adjust it for the intended network when necessary. This lookup selects a local address for that route; it does not verify that a remote application is listening. The outgoing message destination is supplied separately to `UDPSend()`.

## Helper Methods

| Method                               | Behavior                                                                                                                 |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| `SocketHelper()`                     | Looks up and stores `self.local_ip`.                                                                                     |
| `get_local_ip_address()`             | Returns the selected local IP address, or `None` after a socket error.                                                   |
| `UDPSend(cmd, targetIP, targetPort)` | Encodes a text command and attempts to transmit it to the specified destination.                                         |
| `UDPReceive(IP=None, PORT=None)`     | Binds a local socket and returns `(message, sender_ip, sender_port)` for one received message; otherwise returns `None`. |
| `return_ip()`                        | Performs another local-IP lookup and returns the result without updating the cached `self.local_ip`.                     |

Pass port numbers as integers. The `IP` argument to `UDPReceive()` must identify an interface on the receiving machine, while `targetIP` identifies the destination machine.

## Implementation Notes

> [!IMPORTANT]
> The supplied `UDPSend()` method calls `sendto()` twice, including once inside `print()`. A successful invocation therefore attempts to send the same message twice. To send once, store the result of a single `sendto()` call and print that stored byte count.

- **Explicit receive addresses require a port.** The default-port assignment is nested inside `if IP is None`. Calling `UDPReceive(IP="...")` alone leaves `PORT` unset; pass both `IP` and `PORT` when specifying a local address.
- **Receiving is one call at a time.** The helper closes its socket after receiving one datagram or encountering a timeout/error. Continuous reception requires additional application logic.
- **Errors are suppressed.** Send and receive methods use bare `except` blocks. `None` from the receiver can mean a timeout, binding failure, decoding failure, or another error. The send method provides no success/failure return value.
- **GUI responsiveness needs coordination.** The helper contains no background worker. Calling its blocking receive method directly from a GUI callback can pause the interface while it waits.
- **Messages should fit the receive buffer.** Keep text within 1,024 UTF-8 encoded bytes for this implementation. Longer datagrams are not reassembled by the helper.
- **Sender ports can differ from listening ports.** Sending uses a new socket without an explicit local bind, so the observed source port need not be `6000`.

UDP communication does not guarantee delivery, ordering, or duplicate protection. A printed `sent` message is not an acknowledgment from the receiver. See the [UDP specification](https://www.rfc-editor.org/rfc/rfc768).

## Troubleshooting

| Issue                              | What to check                                                                                            |
| ---------------------------------- | -------------------------------------------------------------------------------------------------------- |
| No local address is returned       | Check the active network interface and the configured lookup destination.                                |
| No message is received             | Confirm the target address and port, an active receive call, and firewall rules for the chosen UDP port. |
| Messages appear twice              | Check the two `sendto()` calls in `UDPSend()`.                                                           |
| Receiving fails with a supplied IP | Pass an integer port too, and bind to an address belonging to the receiving machine.                     |
| The interface briefly freezes      | Move blocking network work out of the GUI event callback and coordinate results with the GUI event loop. |
