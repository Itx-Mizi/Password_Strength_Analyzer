#!/usr/bin/env python3
# Simple TCP Port Scanner

import socket
from datetime import datetime

# Display banner
print(r"""
   ________            _____                                 
  /_  __/ /_  ___     / ___/_________ _____  ____  ___  _____
   / / / __ \/ _ \    \__ \/ ___/ __ `/ __ \/ __ \/ _ \/ ___/
  / / / / / /  __/   ___/ / /__/ /_/ / / / / / / /  __/ /
 /_/ /_/ /_/\___/   /____/\___/\__,_/_/ /_/_/ /_/\___/_/

              Advanced TCP Port Scanner
""")

# Target IP
target = input("Enter Target IP Address: ")

# Port range
start_port = int(input("Start Port: "))
end_port = int(input("End Port: "))

print(f"\n[*] Scanning {target}")
print(f"[*] Time Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

print("=" * 60)

for port in range(start_port, end_port + 1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    result = sock.connect_ex((target, port))

    if result == 0:
        print(f"[+] Port {port:<5} OPEN")

    sock.close()

print("=" * 60)
print(f"[*] Scan Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
