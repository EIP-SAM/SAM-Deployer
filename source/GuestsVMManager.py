import ntpath
from VMController import *
from ScriptsLibrary import *

class GuestsVMManager:
    _verbose = None
    _configFile = None
    _listInstr = None
    _makeInstr = None
    _scriptsLib = None
    _SHARED_FOLDER_NAME = "sam"
    _TMP_DIR = {
        "linux" : "/tmp/",
        "windows" : "C:\\Users\\Sam\\Desktop\\"
    }

    def __init__(self, verbose, configFile, listInstr, makeInstr):
        self._verbose = verbose
        self._configFile = configFile
        self._listInstr = listInstr
        self._makeInstr = makeInstr
        self._scriptsLib = ScriptsLibrary()

    def run(self):
        if (self._listInstr != None):
            self.list()
        if (self._makeInstr != None):
            self.make()

    #
    ## VM aliases and paths management
    def linkVMAliasesAndPaths(self, vmAliases, vmPaths):
        vmDict = {}

        for vmAlias in vmAliases:
            vmDict[vmAlias] = None
            for vmPath in vmPaths:
                path, file = os.path.split(vmPath)
                fileName, fileExtension = os.path.splitext(file)
                if (fileName == vmAlias):
                    vmDict[vmAlias] = vmPath
                    break
        return vmDict

    def getAllVMAliasesAndPaths(self, vmPaths):
        vmDict = {}

        for vmPath in vmPaths:
            path, file = os.path.split(vmPath)
            fileName, fileExtension = os.path.splitext(file)
            vmDict[fileName] = vmPath
        return vmDict

    #
    ## --list management
    def list(self):
        print("List Instructions =\t" + str(self._listInstr))

        vmAP = self.linkVMAliasesAndPaths(self._listInstr["vm_aliases"],
                                          self._configFile["vm-paths"])
        print(vmAP)

    #
    ## --make management
    def make(self):
        # print("Make Instructions =\t" + str(self._makeInstr))

        if (len(self._makeInstr["vm_aliases"]) == 1 and self._makeInstr["vm_aliases"] == ["all"]):
            vmAP = self.getAllVMAliasesAndPaths(self._configFile["vm-paths"])
            for vmAlias in vmAP:
                self.makeOnGuest(vmAlias, vmAP[vmAlias])
        else:
            vmAP = self.linkVMAliasesAndPaths(self._makeInstr["vm_aliases"],
                                              self._configFile["vm-paths"])
            for vmAlias in self._makeInstr["vm_aliases"]:
                self.makeOnGuest(vmAlias, vmAP[vmAlias])

    #
    ## Execute --make on guests
    def makeOnGuest(self, vmAlias, vmPath):
        vm = VMController(vmPath)

        print("Starting \"" + vmAlias + "\" virtual environment")
        print("Location : \"" + vmPath + "\"")
        print("Please wait...")

        vm.start()
        vmOS = vm.getGuestOperatingSystem()
        print("Virtual environment successfuly started")

        vm.enableSharedFolders()

        for project in self._configFile["projects"]:
            print("\tSharing project " + project["name"] + " with virtual environment")
            print("\tLocation on host : \"" + project["root-folder"] + "\"")

            vm.addSharedFolder(self._SHARED_FOLDER_NAME, project["root-folder"])
            hostScriptLocation = self._scriptsLib.scripts[vmOS]["mount_shared_folder"]
            guestScriptLocation = self._TMP_DIR[vmOS] + ntpath.basename(hostScriptLocation)
            vm.copyFileFromHostToGuest(hostScriptLocation, guestScriptLocation)
            vm.runProgramInGuest(guestScriptLocation)

            input("\tPress Enter to continue...")

            vm.deleteFileInGuest(guestScriptLocation)

            hostScriptLocation = self._scriptsLib.scripts[vmOS]["unmount_shared_folder"]
            guestScriptLocation = self._TMP_DIR[vmOS] + ntpath.basename(hostScriptLocation)
            vm.copyFileFromHostToGuest(hostScriptLocation, guestScriptLocation)
            vm.runProgramInGuest(guestScriptLocation)
            vm.deleteFileInGuest(guestScriptLocation)
            vm.removeSharedFolder(self._SHARED_FOLDER_NAME)
            print()

        print("Pausing virtual environment")
        print("Please wait...")
        vm.suspend()
        print("Virtual environment successfuly paused")
        print()
