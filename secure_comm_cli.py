#!/usr/bin/env python3

import sys
import os

PID_FILE = "/tmp/sc_server.pid"

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

    if command == "status":
   	 status()
    elif command == "help":
   	 show_help()
    else:
   	 print(f"Command '{command}' not implemented yet")

	
if __name__ == "__main__":
    main()
