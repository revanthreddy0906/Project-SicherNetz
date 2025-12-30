import socket
import ssl
import threading
import sys

SERVER_HOST = "100.31.44.180"   # your EC2 public IP
SERVER_PORT = 8443

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print("\n" + data.decode())
        except:
            break

def main():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with socket.create_connection((SERVER_HOST, SERVER_PORT)) as sock:
        with context.wrap_socket(sock) as ssock:
            print("[+] Secure TLS connection established")

            username = input("Username: ").strip()
            password = input("Password: ").strip()

            ssock.sendall(f"{username}:{password}".encode())

            response = ssock.recv(1024).decode()
            if not response.startswith("OK"):
                print("❌ Authentication failed")
                return

            _, group = response.split(":", 1)
            print(f"✔ Logged in successfully (Group: {group})")
            print("Type messages. Type 'exit' to logout.")

            # ---- START RECEIVER THREAD ----
            recv_thread = threading.Thread(
                target=receive_messages,
                args=(ssock,),
                daemon=True
            )
            recv_thread.start()

            # ---- SEND LOOP ----
            while True:
                msg = input()
                ssock.sendall(msg.encode())

                if msg.lower() == "exit":
                    print("👋 Logged out")
                    break

if __name__ == "__main__":
    main()
