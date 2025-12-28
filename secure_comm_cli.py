#!/usr/bin/env python3

import sys
import subprocess
import os
import signal


PID_FILE = "/tmp/sc_server.pid"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVER_FILE = os.path.join(BASE_DIR, "server.py")

def start():
    if os.path.exists(PID_FILE):
        print("⚠️ secure-comm server is already running")
        return

    process = subprocess.Popen(
        ["python3", SERVER_FILE],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    with open(PID_FILE, "w") as f:
        f.write(str(process.pid))

    print(f"🟢 secure-comm server started (PID {process.pid})")

def stop():
    if not os.path.exists(PID_FILE):
        print("⚠️ secure-comm server is not running")
        return

    try:
        with open(PID_FILE, "r") as f:
            pid = int(f.read())

        os.kill(pid, signal.SIGTERM)
        os.remove(PID_FILE)

        print("🛑 secure-comm server stopped")

    except ProcessLookupError:
        os.remove(PID_FILE)
        print("⚠️ Stale PID file removed")

    except Exception as e:
        print(f"❌ Failed to stop server: {e}")


def status():
    if os.path.exists(PID_FILE):
        print("🟢 secure-comm server is running")
    else:
        print("🔴 secure-comm server is not running")


def show_help():
    print("""
sc — Secure Communication CLI

Usage:
  sc start      Start secure-comm server
  sc stop       Stop secure-comm server
  sc status     Show server status
  sc connect    Connect client
  sc help       Show this help
""")

def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1]

    if command == "start":
    	start()
    elif command == "stop":
    	stop()
    elif command == "status":
    	status()
    elif command == "help":
    	show_help()
    else:
    	print(f"Command '{command}' not implemented yet")	


if __name__ == "__main__":
    main()
