from VMController import *

class GuestsVMManager:
    _verbose = None
    _configFile = None
    _listInstr = None
    _makeInstr = None

    def __init__(self, verbose, configFile, listInstr, makeInstr):
        self._verbose = verbose
        self._configFile = configFile
        self._listInstr = listInstr
        self._makeInstr = makeInstr

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
        print("Make Instructions =\t" + str(self._makeInstr))

        if (len(self._makeInstr["vm_aliases"]) == 1 and self._makeInstr["vm_aliases"] == ["all"]):
            vmAP = self.getAllVMAliasesAndPaths(self._configFile["vm-paths"])
            for vmAlias in vmAP:
                self.makeOnGuest(vmAlias, vmAP[vmAlias])
        else:
            vmAP = self.linkVMAliasesAndPaths(self._makeInstr["vm_aliases"],
                                              self._configFile["vm-paths"])
            for vmAlias in self._makeInstr["vm_aliases"]:
                self.makeOnGuest(vmAlias, vmAP[vmAlias])

    def makeOnGuest(self, vmAlias, vmPath):
        vm = VMController(vmPath)

        print(vmAlias + "\t<--> " + str(vmPath))

        vm.start()
        # vm.enableSharedFolders()
        # vm.addSharedFolder("sharedCode", "/home/nicolas")

        input("Press Enter to continue...")

        # vm.removeSharedFolder("sharedCode")
        vm.suspend()

        # print("finished\n")
