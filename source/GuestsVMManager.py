from VMController import *
from ScriptsLibrary import *

class GuestsVMManager:
    _SHARED_FOLDER_NAME = "sam" # Don't forgot to update the other occurences in `scripts_library`

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

        print("######### Starting \"" + vmAlias + "\" virtual environment #########")
        print("Location : \"" + vmPath + "\"")
        print("Please wait...")

        if (vm.start()):
            print("Virtual environment successfuly started")

            if (vm.enableSharedFolders()):
                print("Shared folders successfuly enabled on guest\n")

                for project in self._configFile["projects"]:
                    self.makeProjectOnGuest(vm, project)
                    print()
            else:
                print()

            print("Pausing virtual environment\nPlease wait...")
            if (vm.suspend()):
                print("Virtual environment successfuly paused\n")
            else:
                print("Error: An error occured while trying to pause guest\n")

    #
    ## Compile one project on one guest
    def makeProjectOnGuest(self, vm, project):
        print("%%%%%%%%% Sharing project " + project["name"] + " with virtual environment %%%%%%%%%")
        print("Location on host : \"" + project["root-folder"] + "\"")

        vm.addSharedFolder(self._SHARED_FOLDER_NAME, project["root-folder"])
        vm.executeProgramInGuestFromHost(self._scriptsLib.scripts[vm.os()]["mount_shared_folder"])

        # input("Press Enter to continue...")

        vm.executeProgramInGuestFromHost(self._scriptsLib.scripts[vm.os()]["unmount_shared_folder"])
        vm.removeSharedFolder(self._SHARED_FOLDER_NAME)

    #
    ## --tests management
    def compileAndExecuteUnitTests(self):
        print("Hey, je suis sense lancer les vms une par une, compiler et executer les tests unitaires")
        print("Mais en vrai je fais rien")
        print("Pour l'instant")
