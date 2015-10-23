#!/usr/bin/env python3

import platform

if (platform.system() == "Linux"):
    open("/tmp/SUCCESS", 'a').close()
else:
    open("C:\\Users\\Sam\\Desktop\\SUCCESS", 'a').close()

print("Hello world ! 8 )")

exit(0)
