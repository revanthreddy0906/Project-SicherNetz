#!/usr/bin/env python3

import sys
import subprocess
import os
import signal

CONFIG_DIR = os.path.expanduser("~/.secure-comm")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config")

def ensure_config_dir():
    os.makedirs(CONFIG_DIR, exist_ok=True)


def read_config():
    if not os.path.exists(CONFIG_FILE):
        return {}

    config = {}
    with open(CONFIG_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line or "=" not in line:
                continue
            key, value = line.split("=", 1)
            config[key] = value
    return config


def write_config(key, value):
    ensure_config_dir()
    config = read_config()
    config[key] = value

    with open(CONFIG_FILE, "w") as f:
        for k, v in config.items():
            f.write(f"{k}={v}\n")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SERVER_FILE = os.path.join(BASE_DIR, "server", "server.py")
CLIENT_FILE = os.path.join(BASE_DIR, "client", "client.py")

PID_FILE = "/tmp/sc_server.pid"


def connect(server_ip=None):
    if not os.path.exists(PID_FILE):
        print("❌ Server is not running. Use: sc start")
        return

    try:
        with open(PID_FILE, "r") as f:
            pid = int(f.read())

        # Check if process actually exists
        os.kill(pid, 0)

    except ProcessLookupError:
        print("❌ Server PID is stale. Restart the server using: sc start")
        return

    except Exception as e:
        print(f"❌ Unable to verify server state: {e}")
        return

    env = os.environ.copy()

    if server_ip:
    	env["SC_SERVER_HOST"] = server_ip

    subprocess.run(["python3", CLIENT_FILE], env=env)


def start():
    if os.path.exists(PID_FILE):
        print("⚠️ secure-comm server is already running")
        return

    print("⚠️ Note: sc start should be run only on the central server (EC2/admin machine).")

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
    server_ip = None

    if "--server" in sys.argv:
        idx = sys.argv.index("--server")
        try:
            server_ip = sys.argv[idx + 1]
        except IndexError:
            print("❌ Missing IP after --server")
            return

    if command == "start":
        start()
    elif command == "stop":
        stop()
    elif command == "status":
        status()
    elif command == "connect":
        connect(server_ip)
    elif command == "help":
        show_help()
    else:
        print(f"Command '{command}' not implemented yet")



if __name__ == "__main__":
    main()
