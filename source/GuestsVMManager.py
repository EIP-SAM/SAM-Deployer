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
        if (self._testsInstr != None):
            self.compileAndExecuteUnitTests()

    #
    ## VM aliases and paths management
    def linkVMAliasesAndPaths(self, vmAliases, virtualMachines):
        vmDict = {}

        for vmAlias in vmAliases:
            vmDict[vmAlias] = None
            for vm in vms:
                if ((vm["alias"] == vmAlias) and (vm["path"] is not None)):
                    vmDict[vmAlias] = vm["path"]
                    break
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

    #
    ## --tests management
    def compileAndExecuteUnitTests(self):
        print("Hey, je suis sense lancer les vms une par une, compiler et executer les tests unitaires")
        print("Mais en vrai je fais rien")
        print("Pour l'instant")
