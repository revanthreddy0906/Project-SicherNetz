import socket
import ssl
import os
import threading
from db import init_db, authenticate

HOST = "0.0.0.0"
PORT = 8443

# -------- INIT DB --------
init_db()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CERT_DIR = os.path.join(BASE_DIR, "..", "certs")

# -------- TLS CONTEXT --------
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(
    certfile=os.path.join(CERT_DIR, "server.crt"),
    keyfile=os.path.join(CERT_DIR, "server.key")
)

# -------- GROUP SESSIONS --------
group_sessions = {}      # group -> list of connections
session_users = {}       # connection -> username
lock = threading.Lock()

def broadcast(group, message, sender_conn=None):
    with lock:
        for conn in group_sessions.get(group, []):
            if conn != sender_conn:
                try:
                    conn.sendall(message.encode())
                except:
                    pass

def handle_client(conn, addr):
    print(f"[+] Connection from {addr}")

    try:
        # ---- RECEIVE CREDENTIALS ----
        data = conn.recv(1024).decode().strip()
        print("[AUTH DATA]", data)

        try:
            username, password = data.split(":", 1)
        except ValueError:
            conn.sendall(b"AUTH_FAILED")
            conn.close()
            return

        group = authenticate(username, password)

        if not group:
            conn.sendall(b"AUTH_FAILED")
            print(f"[-] Auth failed for {addr}")
            conn.close()
            return

        conn.sendall(f"OK:{group}".encode())
        print(f"[+] {username} authenticated (Group: {group})")

        # ---- REGISTER SESSION ----
        with lock:
            group_sessions.setdefault(group, []).append(conn)
            session_users[conn] = username

        broadcast(group, f"[SYSTEM] {username} joined the group", conn)

        # ---- CHAT LOOP ----
        while True:
            data = conn.recv(1024)
            if not data:
                break

            msg = data.decode().strip()
            if msg.lower() == "exit":
                break

            formatted = f"[{group}] {username}: {msg}"
            print(formatted)
            broadcast(group, formatted, conn)

    except Exception as e:
        print(f"[!] Error: {e}")

    finally:
        # ---- CLEANUP ----
        with lock:
            group = next(
                (g for g, conns in group_sessions.items() if conn in conns),
                None
            )
            if group:
                group_sessions[group].remove(conn)
                broadcast(group, f"[SYSTEM] {session_users.get(conn)} left the group", conn)

            session_users.pop(conn, None)

        conn.close()
        print(f"[-] Connection closed {addr}")

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(5)

    print(f"[SECURE SERVER] Listening on port {PORT}")

    while True:
        client, addr = sock.accept()
        secure_conn = context.wrap_socket(client, server_side=True)
        threading.Thread(
            target=handle_client,
            args=(secure_conn, addr),
            daemon=True
        ).start()

if __name__ == "__main__":
    main()
