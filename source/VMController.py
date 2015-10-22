import os
import sys
import platform
import ntpath
from io import StringIO
from subprocess import call
from subprocess import check_output

class VMController:
    _USERNAME = "sam"
    _PASSWORD = "s@m"
    _TMP_DIR = {
        "linux" : "/tmp/",
        "windows" : "C:\\Users\\Sam\\Desktop\\"
    }

    _vmxPath = None
    _os = None

    def __init__(self, vmxPath):
        self._vmxPath = vmxPath

    def start(self):
        return call(["vmrun", "start", self._vmxPath]) == 0

    def suspend(self):
        return call(["vmrun", "suspend", self._vmxPath]) == 0

    def _getGuestOperatingSystem(self):
        path = self.readEnvironmentVariable("PATH")
        if ((type(path) is str) and (len(path) > 0)):
            if (path[0] == '/'):
                return "linux"
            else:
                return "windows"
        return None

    def os(self):
        self._os = self._os if self._os != None else self._getGuestOperatingSystem()
        return self._os

    def readEnvironmentVariable(self, varName):
        return check_output(["vmrun", "-gu", self._USERNAME, "-gp", self._PASSWORD,
                             "readVariable", self._vmxPath, "guestEnv", varName,
                             ";", "exit", "0"]).decode("utf-8")

    def executeProgramInGuestFromHost(self, hostProgramPath):
        guestProgramPath = self._TMP_DIR[self.os()] + ntpath.basename(hostProgramPath)

        if (self.copyFileFromHostToGuest(hostProgramPath, guestProgramPath)):
            ret = self.runProgramInGuest(guestProgramPath)
            if (self.deleteFileInGuest(guestProgramPath) == False):
                print("Error: An error occured while deleting temporary program in guest")
            return ret
        else:
            print("Error: An error occured while copying temporary program in guest")
        return None

    def copyFileFromHostToGuest(self, hostPath, guestPath):
        return call(["vmrun", "-gu", self._USERNAME, "-gp", self._PASSWORD,
                     "copyFileFromHostToGuest", self._vmxPath, hostPath, guestPath]) == 0

    def copyFileFromGuestToHost(self, guestPath, hostPath):
        return call(["vmrun", "-gu", self._USERNAME, "-gp", self._PASSWORD,
                     "copyFileFromGuestToHost", self._vmxPath, guestPath, hostPath]) == 0

    def deleteFileInGuest(self, filePath):
        return call(["vmrun", "-gu", self._USERNAME, "-gp", self._PASSWORD,
                     "deleteFileInGuest", self._vmxPath, filePath]) == 0

    def directoryExistsInGuest(self, directoryPath):
        return call(["vmrun", "-gu", self._USERNAME, "-gp", self._PASSWORD,
                     "directoryExistsInGuest", directoryPath]) == 0

    def createDirectoryInGuest(self, directoryPath):
        return call(["vmrun", "-gu", self._USERNAME, "-gp", self._PASSWORD,
                     "createDirectoryInGuest", directoryPath]) == 0

    def deleteDirectoryInGuest(self, directoryPath):
        return call(["vmrun", "-gu", self._USERNAME, "-gp", self._PASSWORD,
                     "deleteDirectoryInGuest", directoryPath]) == 0

    def enableSharedFolders(self):
        return call(["vmrun", "enableSharedFolders", self._vmxPath]) == 0

    def addSharedFolder(self, shareName, hostPath):
        return call(["vmrun", "addSharedFolder", self._vmxPath, shareName, hostPath]) == 0

    def removeSharedFolder(self, shareName):
        return call(["vmrun", "removeSharedFolder", self._vmxPath, shareName]) == 0

    def runProgramInGuest(self, programPath):
        return call(["vmrun", "-gu", self._USERNAME, "-gp", self._PASSWORD,
                     "runProgramInGuest", self._vmxPath, programPath])

    def runScriptInGuest(self, interpreterPath, scriptPath):
        return call(["vmrun", "-gu", self._USERNAME, "-gp", self._PASSWORD,
                     "runScriptInGuest", self._vmxPath, interpreterPath, scriptPath])
