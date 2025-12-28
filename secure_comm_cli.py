#!/usr/bin/env python3

import sys

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

    if command == "help":
        show_help()
    else:
        print(f"Command '{command}' not implemented yet")

if __name__ == "__main__":
    main()
