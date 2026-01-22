import socket
import threading
import argparse  #

# --------- Colors (ANSI escape codes) ----------
RESET = "\033[0m"
GREEN = "\033[32m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
YELLOW = "\033[33m"
RED = "\033[31m"

def send_line(sock, line: str):
    """Send one IRC line. IRC requires lines to end with \\r\\n."""
    sock.sendall((line + "\r\n").encode("utf-8", errors="ignore"))

def recv_thread(sock, state, stop_flag):
    """
    Runs in a separate thread.
    - Receives messages from the IRC server
    - Replies to PING with PONG
    - Prints chat messages (PRIVMSG) nicely
    """
    buffer = ""

    while not stop_flag["stop"]:
        data = sock.recv(4096)
        if not data:
            print(f"{RED}Disconnected by server{RESET}", flush=True)
            stop_flag["stop"] = True
            break

        buffer += data.decode("utf-8", errors="ignore")

        # Process complete lines (IRC messages end with \r\n)
        while "\r\n" in buffer:
            line, buffer = buffer.split("\r\n", 1)
            if not line:
                continue

            # 1) Mandatory: respond to PING
            if line.startswith("PING"):
                token = line.split(":", 1)[1] if ":" in line else ""
                send_line(sock, f"PONG :{token}")
                print(f"{YELLOW}PING -> PONG{RESET}", flush=True)
                continue

            # 2) Show messages
            # Example: :nick!user@host PRIVMSG #chan :hello
            if " PRIVMSG " in line:
                prefix = line[1:].split(" ", 1)[0] if line.startswith(":") else "?"
                nick = prefix.split("!", 1)[0]
                msg = line.split(" :", 1)[1] if " :" in line else ""
                print(f"{CYAN}<{nick}>{RESET} {msg}", flush=True)
                continue

            # 3) Show joins (optional but nice)
            if " JOIN " in line:
                prefix = line[1:].split(" ", 1)[0] if line.startswith(":") else "?"
                nick = prefix.split("!", 1)[0]
                ch = line.split(" :", 1)[1] if " :" in line else (line.split()[-1] if line.split() else "")
                print(f"{GREEN}* {nick} joined {ch}{RESET}", flush=True)
                continue

            # Everything else: ignore safely (task requirement)

def main():
    ap = argparse.ArgumentParser(description="Minimal IRC client (colors only)")
    ap.add_argument("--server", default="irc.libera.chat")
    ap.add_argument("--port", type=int, default=6667)
    ap.add_argument("--nick", default="sethi_test")
    ap.add_argument("--channel", default="#gdg-test")
    ap.add_argument("--realname", default="Sethi Ji")
    args = ap.parse_args()

    state = {"channel": args.channel} #We store the current channel in a dictionary called state

    print(f"{GREEN}Connecting to {args.server}:{args.port} ...{RESET}", flush=True)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    '''
    This creates the TCP socket object.
    AF_INET = internet addresses (like irc.libera.chat)
    SOCK_STREAM = TCP (reliable connection)
    '''
    sock.connect((args.server, args.port))
    print(f"{GREEN}Connected ✅{RESET}", flush=True)

    # Handshake (required by IRC)
    send_line(sock, f"NICK {args.nick}")
    send_line(sock, f"USER {args.nick} 0 * :{args.realname}")

    # Start receiver thread so we can receive while typing
    stop_flag = {"stop": False}
    t = threading.Thread(target=recv_thread, args=(sock, state, stop_flag), daemon=True)
    t.start()
    '''
    daemin=True means if the main program exits,this thread wont keep the process alive
    '''

    # Join initial channel
    send_line(sock, f"JOIN {state['channel']}")
    print(f"{GREEN}Joined {state['channel']}{RESET}", flush=True)

    try:
        while not stop_flag["stop"]:
            user = input().strip()
            if not user:
                continue

            if user.startswith("/quit"):
                send_line(sock, "QUIT :bye")
                print(f"{RED}Quitting...{RESET}", flush=True)
                break

            if user.startswith("/join "):
                parts = user.split(maxsplit=1)
                if len(parts) == 2 and parts[1].strip():
                    state["channel"] = parts[1].strip()
                    send_line(sock, f"JOIN {state['channel']}")
                    print(f"{GREEN}Joined {state['channel']}{RESET}", flush=True)
                continue

            # Normal message -> send to current channel
            send_line(sock, f"PRIVMSG {state['channel']} :{user}")
            print(f"{MAGENTA}<you>{RESET} {user}", flush=True)

    except (KeyboardInterrupt, EOFError):
        try:
            send_line(sock, "QUIT :bye")
        except OSError:
            pass
    finally:
        stop_flag["stop"] = True
        try:
            sock.close()
        except OSError:
            pass

if __name__ == "__main__":
    main()
