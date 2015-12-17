#!/usr/bin/env python3

import socket
import sys

if (len(sys.argv) != 2 + 1):
    print("Wrong number of arguments")
    exit(1)

ip = sys.argv[0:][1]
port = int(sys.argv[0:][2])

print("Retrieving host ip address")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen(2)

# print("Waiting for 1st incoming connexion...")
# (client_socket, client_address) = server.accept()
# print("Client connected!")
# data = client_socket.recv(8)
# str_data = data.decode("utf-8")
# print("client1 id = " + str_data)

# if (str_data == "local"):
#     client_socket.send("ok".encode("utf-8"))
# else:
#     print("Incoming data = \"" + str_data + "\"")

# print("Waiting for 2nd incoming connexion...")
# (client_socket2, client_address2) = server.accept()
# print("Client connected!")
# data2 = client_socket2.recv(8)
# str_data2 = data2.decode("utf-8")
# print("client2 id = " + str_data2)

# if (str_data2 == "local"):
#     client_socket2.send("ok".encode("utf-8"))
# else:
#     print("Incoming data = \"" + str_data + "\"")

def acceptNewClient(server):
    print("Waiting for incoming connexion...")
    (client_socket, client_address) = server.accept()
    print("Client connected!")
    data = client_socket.recv(8)
    str_data = data.decode("utf-8")
    print("client1 id = " + str_data)

    if (str_data == "local"):
        client_socket.send("ok".encode("utf-8"))
    else:
        print("Incoming data = \"" + str_data + "\"")
    return (client_socket, client_address, str_data)

(client_socket, client_address, client_id) = acceptNewClient(server)
(client_socket2, client_address2, client_id2) = acceptNewClient(server)

host_socket = None
host_ip = None

if (client_id == "host"):
    host_socket = client_socket
    host_ip = client_address[0]
elif (client_id2 == "host"):
    host_socket = client_socket2
    host_ip = client_address2[0]
else:
    print("Error: Invalid answer")
    exit(21)

# if (str_data == "host"):
#     host_socket = client_socket
#     host_ip = client_address[0]
# elif (str_data2 == "host"):
#     host_socket = client_socket2
#     host_ip = client_address2[0]
# else:
#     print("Error: Invalid answer")
#     exit(21)

if (host_socket != None):
    host_socket.send(host_ip.encode("utf-8"))
else:
    exit(42)

print(str(host_ip))

server.shutdown(0)
server.close()

exit(0)
