# Gdg-Task-2
# Task 2 – Minimal IRC Client

## Task Description
The task was to build a minimal IRC client using raw TCP sockets that can connect to a real IRC server, join a channel, and allow message exchange through the terminal.

---

## My Understanding of the Task
IRC is a text-based chat protocol.  
The client needs to:
- Open a TCP connection to an IRC server
- Send basic IRC commands like `NICK`, `USER`, and `JOIN`
- Read messages sent by the server
- Send messages using `PRIVMSG`
- Reply to server `PING` messages with `PONG`

---

## Approach I Planned to Follow
If I had more time, I would implement the client in these steps:

1. Create a TCP socket using Python’s `socket` module  
2. Connect to the IRC server and port provided by the user  
3. Perform the IRC handshake using `NICK` and `USER`  
4. Continuously read messages from the server  
5. Handle `PING → PONG` to keep the connection alive  
6. Join a single channel and send messages  
7. Allow basic user commands like `/join` and `/quit`  
8. Add simple improvements like timestamps and colored output

---

## Current Status
Due to time constraints, I could not implement the code yet.  
However, I focused on understanding the IRC protocol and planning a clean step-by-step implementation.

---

## References
- https://modern.ircdocs.horse/
- RFC 1459
- Python socket documentation
