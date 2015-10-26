#!/usr/bin/env python3

import platform
import sys
import os
from subprocess import call

if (len(sys.argv) != 2 + 1):
    print("Wrong number of arguments")
    exit(1)

if (platform.system() == "Linux"):
    shared_folder = "/home/sam/mnt/"
    project_file = shared_folder + sys.argv[1]
else:
    shared_folder = "Z:\\"
    project_file = shared_folder + sys.argv[1].replace("/", "\\")

build_dir = sys.argv[2]

os.chdir(shared_folder)

tmp = os.path.dirname(os.path.dirname(project_file))
tmp = tmp if len(tmp) > 0 else "."
os.chdir(tmp)

os.mkdir(build_dir)
os.chdir(build_dir)

if (platform.system() == "Linux"):
    call(["qmake", project_file, "-r", "-spec", "linux-g++", "CONFIG+=DEBUG"])
    call(["make"])
else:
    call(["qmake", project_file, "-r", "-spec", "win32-msvc2013", "CONFIG+=DEBUG"])
    call(["cmd", "/c", "C:\\Program Files (x86)\\Microsoft Visual Studio 12.0\\VC\\vcvarsall.bat", "amd64", "&&", "jom", "-f", "Makefile.Debug"])

exit(0)
