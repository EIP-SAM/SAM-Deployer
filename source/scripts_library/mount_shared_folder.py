#!/usr/bin/env python3

import platform
from subprocess import call

if (platform.system() == "Linux"):
    ret = call(["sh", "-c", "echo s@m | sudo -S " +
                "mount -n -t vmhgfs .host:/sam /home/sam/mnt"])
elif (platform.system() == "Windows"):
    ret = call(["net", "use", "z:", "\\\\vmware-host\\Shared Folders\\sam"])

exit(ret)
