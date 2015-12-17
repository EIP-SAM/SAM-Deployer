import os
import platform
import socket
from VMController import *
from ScriptsLibrary import *
from GuestStdoutReceiver import *

class GuestsVMManager:
    _HOST_TMP_DIR = "/tmp/" if platform.system() != "Windows" else os.environ["TMP"] + "\\"
    _SHARED_FOLDER_NAME = "sam" # Don't forgot to update the other occurences in `scripts_library`
    _PYTHON_INTERPRETER = {
        "linux" : "/usr/bin/python3",
        "windows" : "C:\\Python3\\python.exe"
    }

    _verbose = None
    _configFile = None
    _listInstr = None
    _makeInstr = None
    _scriptsLib = None
    _testsInstr = None

    def __init__(self, verbose, configFile, listInstr, makeInstr, testsInstr):
        self._verbose = verbose
        self._configFile = configFile
        self._listInstr = listInstr
        self._makeInstr = makeInstr
        self._testsInstr = testsInstr
        self._scriptsLib = ScriptsLibrary()

    def run(self):
        if (self._listInstr != None):
            self.list()
        if (self._makeInstr != None):
            self.make()
        if (self._testsInstr):
            self.compileAndExecuteUnitTests()

    #
    ## VM aliases and paths management
    def linkVMAliasesAndPaths(self, vmAliases, virtualMachines):
        vmDict = {}

        for vmAlias in vmAliases:
            vmDict[vmAlias] = None
            for vm in virtualMachines:
                if ((vm["alias"] is not None) and
                    (vm["path"] is not None) and (vm["alias"] == vmAlias)):
                    vmDict[vmAlias] = vm["path"]
                    break
        return vmDict

    #
    ## --list management
    def list(self):
        print("List Instructions =\t" + str(self._listInstr) + "\n")

        if (len(self._listInstr) == 1 and self._listInstr[0] == "all"):
            print("######### Listing all virtual environments #########")
            for vm in self._configFile["virtual-machines"]:
                if ((vm["alias"] != None) and (vm["path"] != None)):
                    print("Virtual environment : \"" + vm["alias"] + "\"")
                    print("Location : \"" + vm["path"] + "\"\n")
                else:
                    print("Error: Broken `virtual-machine` object in configuration file")
        else:
            vmAP = self.linkVMAliasesAndPaths(self._listInstr,
                                              self._configFile["virtual-machines"])
            print("######### Listing specified virtual environment(s) #########")
            for vmAlias in self._makeInstr["vm_aliases"]:
                print("Virtual environment : \"" + vmAlias + "\"")
                print("Location : \"" + vmPath + "\"\n")

    #
    ## --make management
    def make(self):
        print("Make Instructions =\t" + str(self._makeInstr) + "\n")

        if (len(self._makeInstr["vm_aliases"]) == 1 and self._makeInstr["vm_aliases"] == ["all"]):
            for vm in self._configFile["virtual-machines"]:
                if ((vm["alias"] != None) and (vm["path"] != None)):
                    self.makeOnGuest(vm["alias"], vm["path"])
                else:
                    print("Error: Broken `virtual-machine` object in configuration file")
        else:
            vmAP = self.linkVMAliasesAndPaths(self._makeInstr["vm_aliases"],
                                              self._configFile["virtual-machines"])
            for vmAlias in self._makeInstr["vm_aliases"]:
                self.makeOnGuest(vmAlias, vmAP[vmAlias])

    #
    ## Compile each project on each guest
    def makeOnGuest(self, vmAlias, vmPath):
        vm = VMController(vmPath)
        hostPort = 42064

        print("######### Starting \"" + vmAlias + "\" virtual environment #########")
        print("Location : \"" + vmPath + "\"")
        print("Please wait...")

        if (vm.start()):
            print("Virtual environment successfuly started")

            if (not vm.enableSharedFolders()):
                print("Trying anyway...")
            else:
                print("Shared folders successfuly enabled on guest")

            hostIp = self.getHostIpAddress(vm)
            hostIp = "" if hostIp == None else hostIp
            guestStdout = GuestStdoutReceiver(hostIp, hostPort)

            print()
            for project in self._configFile["projects"]:
                self.makeProjectOnGuest(vm, vmAlias, project, str(hostPort), hostIp)
                print()

            guestStdout.stop()
            # print("GuestStdout stopped")

            print("Pausing virtual environment\nPlease wait...")
            if (vm.suspend()):
                print("Virtual environment successfuly paused\n")
            else:
                print("Error: An error occured while trying to pause guest\n")

    #
    ## Compile one project on one guest
    def makeProjectOnGuest(self, vm, vmAlias, project, hostPort, hostIp):
        print("%%%%%%%%% Sharing project " + project["name"] + " with virtual environment %%%%%%%%%")
        print("Location on host : \"" + project["root-folder"] + "\"")

        if (not self.projectConfigIsValid(project["qt-project-file"], project["root-folder"])):
            print("Error: `qt-project-file` is not a valid path under `root-folder`\n" +
                  "`qt-project-file`: \"" + project["qt-project-file"] + "\"\n" +
                  "`root-folder`: \"" + project["root-folder"] + "\"")
            return
        fileName, fileExtension = os.path.splitext(project["qt-project-file"])
        if (fileExtension != ".pro"):
            print("Warning: Qt project file, '" + fileName + fileExtension +
                  "', is supposed to have a '.pro' extension. This may not work")

        if (not vm.addSharedFolder(self._SHARED_FOLDER_NAME, project["root-folder"])):
            print("Trying anyway...")
        vm.executeScriptInGuestFromHost(self._PYTHON_INTERPRETER[vm.os()],
                                        self._scriptsLib.scripts["mount_shared_folder"])

        buildDir = "build_" + project["name"].replace(" ", "-") + "_" + vmAlias.replace(" ", "-")
        projectFile = project["qt-project-file"][len(project["root-folder"]) + 1:]
        vm.executeScriptInGuestFromHost(self._PYTHON_INTERPRETER[vm.os()],
                                        self._scriptsLib.scripts["make_project"],
                                        projectFile, buildDir, hostIp, hostPort)

        vm.executeScriptInGuestFromHost(self._PYTHON_INTERPRETER[vm.os()],
                                        self._scriptsLib.scripts["unmount_shared_folder"])
        vm.removeSharedFolder(self._SHARED_FOLDER_NAME)

    #
    ## Check if "project" : { "root-folder", "qt-project-file" } paths are valid
    def projectConfigIsValid(self, projectFilePath, projectRootFolder):
        return ((projectFilePath != None and projectRootFolder != None) and
                (type(projectFilePath) == str and type(projectRootFolder) == str) and
                (len(projectFilePath) > 0 and len(projectRootFolder) > 0) and
                (len(projectFilePath) > len(projectRootFolder)) and
                (projectFilePath[:len(projectRootFolder)] == projectRootFolder) and
                os.path.isfile(projectFilePath))

    #
    ## --tests management
    def compileAndExecuteUnitTests(self):
        print("Hey, je suis sense lancer les vms une par une, compiler et executer les tests unitaires")
        print("Mais en vrai je fais rien")
        print("Pour l'instant")

    def getHostIpAddress(self, vm):
        port = 42021
        guestIp = self.getGuestIpAddress(vm)

        if (guestIp == None):
            return None
        if (vm.executeScriptInGuestFromHostNoWait(self._PYTHON_INTERPRETER[vm.os()],
                                                  self._scriptsLib.scripts["get_host_ip_address"],
                                                  guestIp, str(port)) == 0):
            # print("Get host ip script launched")
            if (vm.executeScriptInGuestFromHost(self._PYTHON_INTERPRETER[vm.os()],
                                                self._scriptsLib.scripts["wait_for_host_ip"],
                                                guestIp, str(port)) == 0):
                # print("Get host ip script is ready")
                clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # print("Client socket created")
                clientSocket.connect((guestIp, port))
                # print("Connected")
                clientSocket.send("host".encode("utf-8"))
                hostIpBin = clientSocket.recv(32)
                hostIp = str(hostIpBin.decode("utf-8"))
                print("Host IP address is " + hostIp)
                return hostIp
        print("Warning: Failed to retrieve host ip address")
        return None

    def getGuestIpAddress(self, vm):
        guestIpFilePath = vm.getTmpDirectory() + "ip_addr.txt"
        hostTmpGuestIpFilePath = self._HOST_TMP_DIR + "ip_addr.txt"

        if (vm.executeScriptInGuestFromHost(self._PYTHON_INTERPRETER[vm.os()],
                                            self._scriptsLib.scripts["get_guest_ip_address"],
                                            guestIpFilePath) == 0 and
            vm.copyFileFromGuestToHost(guestIpFilePath, hostTmpGuestIpFilePath)):
            guestIp = None
            with open(hostTmpGuestIpFilePath, "r") as ipFile:
                guestIp = ipFile.readline()
            with open(hostTmpGuestIpFilePath, "w") as ipFile:
                ipFile.truncate()
            vm.deleteFileInGuest(guestIpFilePath)
            print("Guest IP address is " + guestIp)
            return guestIp
        print("Warning: Failed to retrieve guest ip address")
        return None
