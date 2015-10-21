import os
import sys
import platform
from io import StringIO
from subprocess import call
from subprocess import check_output

class VMController:
    _vmxPath = None
    _username = "sam"
    _password = "s@m"

    def __init__(self, vmxPath):
        self._vmxPath = vmxPath

    def start(self):
        call(["vmrun", "start", self._vmxPath])

    def suspend(self):
        call(["vmrun", "suspend", self._vmxPath])

    def getGuestOperatingSystem(self):
        path = self.readEnvironmentVariable("PATH")
        if (type(path) is str):
            if (len(path) > 0):
                if (path[0] == '/'):
                    return "linux"
                else:
                    return "windows"
        return None

    def readEnvironmentVariable(self, varName):
        varContent = check_output(["vmrun", "-gu", self._username, "-gp", self._password,
                                   "readVariable", self._vmxPath, "guestEnv", varName,
                                   ";", "exit", "0"])
        return varContent.decode("utf-8")

    def copyFileFromHostToGuest(self, hostPath, guestPath):
        call(["vmrun", "-gu", self._username, "-gp", self._password,
              "copyFileFromHostToGuest", self._vmxPath, hostPath, guestPath])

    def copyFileFromGuestToHost(self, guestPath, hostPath):
        call(["vmrun", "-gu", self._username, "-gp", self._password,
              "copyFileFromGuestToHost", self._vmxPath, guestPath, hostPath])

    def deleteFileInGuest(self, filePath):
        call(["vmrun", "-gu", self._username, "-gp", self._password,
              "deleteFileInGuest", self._vmxPath, filePath])

    def directoryExistsInGuest(self, directoryPath):
        call(["vmrun", "-gu", self._username, "-gp", self._password,
              "directoryExistsInGuest", directoryPath])

    def createDirectoryInGuest(self, directoryPath):
        call(["vmrun", "-gu", self._username, "-gp", self._password,
              "createDirectoryInGuest", directoryPath])

    def deleteDirectoryInGuest(self, directoryPath):
        call(["vmrun", "-gu", self._username, "-gp", self._password,
              "deleteDirectoryInGuest", directoryPath])

    def enableSharedFolders(self):
        call(["vmrun", "enableSharedFolders", self._vmxPath])

    def addSharedFolder(self, shareName, hostPath):
        call(["vmrun", "addSharedFolder", self._vmxPath, shareName, hostPath])

    def removeSharedFolder(self, shareName):
        call(["vmrun", "removeSharedFolder", self._vmxPath, shareName])

    def runProgramInGuest(self, programPath):
        call(["vmrun", "-gu", self._username, "-gp", self._password,
              "runProgramInGuest", self._vmxPath, programPath])

    def runScriptInGuest(self, interpreterPath, scriptPath):
        call(["vmrun", "-gu", self._username, "-gp", self._password,
              "runScriptInGuest", self._vmxPath, interpreterPath, scriptPath])
