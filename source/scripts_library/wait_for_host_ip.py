#!/usr/bin/env python3

import socket
import sys

import time

if (len(sys.argv) != 2 + 1):
    print("Wrong number of arguments")
    exit(1)

ip = sys.argv[0:][1]
port = int(sys.argv[0:][2])

print("Trying to connect to localhost:" + str(sys.argv[0:][1]) + "...")

# time.sleep(2)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created")
# time.sleep(2)
client.connect((ip, port))
print("Client connected")
# time.sleep(2)
print("Sending data...")
client.send("local".encode("utf-8"))
print("Waiting for an answer...")
data = client.recv(8)
data_str = data.decode("utf-8")
print("Answer = \"" + data_str + "\"")
print("Exiting...")

# time.sleep(2)

exit(0)
