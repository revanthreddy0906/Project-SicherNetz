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

def config_cmd(args):
    if not args:
        print("Usage:")
        print("  sc config set <key> <value>")
        print("  sc config show")
        print("  sc config reset")
        return

    action = args[0]

    if action == "set" and len(args) == 3:
        key = args[1]
        value = args[2]
        write_config(key, value)
        print(f"✔ Config set: {key}={value}")

    elif action == "show":
        config = read_config()
        if not config:
            print("No config set.")
            return
        for k, v in config.items():
            print(f"{k}={v}")

    elif action == "reset":
        if os.path.exists(CONFIG_FILE):
            os.remove(CONFIG_FILE)
            print("✔ Config reset")
        else:
            print("No config to reset.")

    else:
        print("Invalid config command.")


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
    print("ℹ️ Server is managed on the admin machine.\n Please Contact the Admin for Access.")


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
  sc config     Configure the Server
  sc help       Show this help
""")

def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1]
    args = sys.argv[2:]

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
    elif command == "config":
    	config_cmd(args)
    else:
        print(f"Command '{command}' not implemented yet")



if __name__ == "__main__":
    main()
