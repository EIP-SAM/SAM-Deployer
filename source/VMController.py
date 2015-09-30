import os
import platform
from subprocess import call

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

    def copyFileFromHostToGuest(self, hostPath, guestPath):
        call(["vmrun", "-gu", self._username, "-gp", self._password,
              "copyFileFromHostToGuest", self._vmxPath, hostPath, guestPath])

    def copyFileFromGuestToHost(self, guestPath, hostPath):
        call(["vmrun", "-gu", self._username, "-gp", self._password,
              "copyFileFromGuestToHost", self._vmxPath, guestPath, hostPath])

    def deleteFileInGuest(self, filePath):
        call(["vmrun", "-gu", self._username, "-gp", self._password,
              "deleteFileInGuest", filePath])

    def enableSharedFolders(self):
        call(["vmrun", "enableSharedFolders", self._vmxPath])

    def addSharedFolder(self, shareName, hostPath):
        call(["vmrun", "addSharedFolder", self._vmxPath, shareName, hostPath])

    def removeSharedFolder(self, shareName):
        call(["vmrun", "removeSharedFolder", self._vmxPath, shareName])

    def runProgramInGuest(self, programPath):
        call("vmrun", "-gu", self._username, "-gp", self._password,
             "runProgramInGuest", self._vmxPath, programPath)

    def runScriptInGuest(self, interpreterPath, scriptPath):
        call("vmrun", "-gu", self._username, "-gp", self._password,
             "runScriptInGuest", self._vmxPath, interpreterPath, scriptPath)
