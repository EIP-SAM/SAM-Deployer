#!/usr/bin/env python3

import platform
import sys
import re
from subprocess import check_output

import time

#
# Quick and dirty main ip getter for guest
# * On windows, the idea is to get the mac address of the
#   default network_adapter, then to get the ip from the mac address
#   In a shell: `net config workstation` + `ipconfig /all`
# * On linux, the idea is to get the default network route, to get
#   the default network adapter name, and then get the ip from the
#   network adapter name
#   In a shell: `route | grep default` + `ip addr`

if (len(sys.argv) != 1 + 1):
    print("Wrong number of arguments")
    exit(1)

output_file = sys.argv[0:][1]

def get_default_net_mac_addr():
    if (platform.system() == "Linux"):
        call([])
    elif (platform.system() == "Windows"):
        net_config = check_output(["net", "config", "workstation"]).decode("utf-8", "ignore")
        pos = net_config.find('(', 0)
        end_pos = net_config.find(')', pos)
        network_adapter_mac = net_config[pos + 1 : end_pos]
        pos = 2
        while (pos < len(network_adapter_mac)):
            network_adapter_mac = network_adapter_mac[:pos] + '-' + network_adapter_mac[pos:]
            pos += 3
        return network_adapter_mac

def get_ip_address(mac_addr):
    if (platform.system() == "Linux"):
        call([])
    elif (platform.system() == "Windows"):
        ip_config = check_output(["ipconfig", "/all"]).decode("utf-8", "ignore")
        pos = 0
        while (pos < len(ip_config)):
            beg_pos = ip_config.find("\r\n\r\n", pos)
            if (beg_pos == -1):
                end_pos = len(ip_config)
            else:
                end_pos = ip_config.find("\r\n\r\n", beg_pos + 4)
            pos = end_pos
            ip_block = ip_config[beg_pos : end_pos]
            if (ip_block.find(mac_addr) != -1):
                pos = 0
                while (pos < len(ip_block)):
                    end_line = ip_block.find("\r\n", pos)
                    line = ip_block[pos : end_line]
                    if (line.find("v4") != -1):
                        ip = re.findall(r"[0-9]+(?:\.[0-9]+){3}", line)
                        if (len(ip) == 1):
                            return ip[0]
                    if (end_line == -1):
                        pos = len(ip_block)
                    else:
                        pos = end_line + 2
                break

print("Retrieving local ip address from default network interface...\n")

ip_addr = None
i = 1

while (ip_addr == None and i != 16):
    print("Test " + str(i) + " of 15")
    if (i > 0):
        time.sleep(1)
    mac_addr = get_default_net_mac_addr()
    ip_addr = get_ip_address(str(mac_addr))
    i += 1

print()
if (ip_addr != None):
    print("MAC : " + mac_addr)
    print("IPv4 : " + ip_addr)
    # time.sleep(2)
else:
    print("Local IP address not found")
    exit(21)

with open(output_file, "w") as file_stream:
    file_stream.truncate()
    file_stream.write(ip_addr)

exit(0)
