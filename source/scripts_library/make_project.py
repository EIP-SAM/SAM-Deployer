#!/usr/bin/env python3

import platform
import socket
import sys
import os
from subprocess import call, Popen, PIPE

import time

if (len(sys.argv) != 4 + 1):
    print("Wrong number of arguments")
    exit(1)

if (platform.system() == "Linux"):
    shared_folder = "/home/sam/mnt/"
    project_file = shared_folder + sys.argv[1]
else:
    shared_folder = "Z:\\"
    project_file = shared_folder + sys.argv[1].replace("/", "\\")

build_dir = sys.argv[2]
host_ip = sys.argv[3]
host_port = int(sys.argv[4])

os.chdir(shared_folder)

tmp = os.path.dirname(os.path.dirname(project_file))
tmp = tmp if len(tmp) > 0 else "."
os.chdir(tmp)

if (os.path.isdir(build_dir) != True):
    os.mkdir(build_dir)

os.chdir(build_dir)

client = None

try:
    print("Trying to connect to log stream receiver " + host_ip + ":" + sys.argv[4] + "...")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host_ip, host_port))
    print("Connected!")
except OSError:
    print("Fatal network error, exiting")
    exit(3)

def winCall(callArgs, socket):
    p = Popen(callArgs, stdout=PIPE, stderr=PIPE)
    while p.poll() is None:
        for line in p.stdout:
            data = line.decode('iso8859-1').replace("\r", "").encode("utf-8")
            socket.send(data)

if (platform.system() == "Linux"):
    print("Configuring platform build file...")
    call(["qmake", project_file, "-r", "-spec", "linux-g++", "CONFIG+=DEBUG"],
         stdout=client, stderr=client)
    print("Building project...")
    call(["make"], stdout=client, stderr=client)
else:
    print("Configuring platform build file...")
    winCall(["qmake", project_file, "-r", "-spec", "win32-msvc2013", "CONFIG+=DEBUG"], client)
    print("Building project...")
    winCall(["cmd", "/c",
             "C:\\Program Files (x86)\\Microsoft Visual Studio 12.0\\VC\\vcvarsall.bat", "amd64",
             "&&", "jom", "-f", "Makefile.Debug"], client)

exit(0)
