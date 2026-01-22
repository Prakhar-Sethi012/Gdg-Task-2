## Gdg Task 2
# Minimal IRC Client (Python, Raw Sockets)

## Overview
This project is a **minimal IRC (Internet Relay Chat) client** implemented in **Python using raw TCP sockets** only.

The client connects to a real IRC server, joins a channel, and allows multiple users to exchange messages through the terminal.  
No IRC libraries or frameworks are used.

This project was built as part of a **GDG coding club task** to understand low-level networking and protocol handling.

---

## Features Implemented
- Connects to a real IRC server using **TCP sockets**
- Performs IRC handshake using `NICK` and `USER`
- Joins a configurable channel
- Sends and receives messages in real time
- Handles server keep-alive using **PING → PONG**
- Supports basic user commands:
  - `/join #channel`
  - `/quit`
- Supports **multiple clients** connecting simultaneously
- Color-coded terminal output for better readability

---

## Technologies Used
- Python 3
- `socket` module (raw TCP networking)
- `threading` (simultaneous input and server listening)
- `argparse` (command-line arguments)

---

## How the Client Works (Simple Explanation)
1. The client opens a TCP connection to an IRC server.
2. It registers itself using `NICK` and `USER` commands.
3. A background thread listens for server messages.
4. The main thread accepts user input from the terminal.
5. Messages typed by the user are sent using `PRIVMSG`.
6. Server `PING` messages are automatically answered with `PONG` to stay connected.

---

## How to Run

### Step 1: Open terminal in the project folder
Make sure you are inside the folder that contains `code.py`.

### Step 2: Run the client
```bash
python code.py --nick SethiJi123 --channel "#gdg-test"
