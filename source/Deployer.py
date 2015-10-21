from GuestsVMManager import *
import json

class Deployer:
    DEFAULT_CONFIG_FILE = "sam-deployer.json"

    _verbose = None
    _infile = None
    _listInstr = None
    _makeInstr = None

    def __init__(self, args):
        self.interpretVerboseArg(args)
        self.interpretInfileArg(args)
        self.interpretListArgs(args)
        self.interpretMakeArgs(args)

    #
    ## Command line arguments interpretation
    def interpretVerboseArg(self, args):
        self._verbose = True if "verbose" in args else False

    def interpretInfileArg(self, args):
        self._infile = args["infile"] if "infile" in args else self.DEFAULT_CONFIG_FILE

    def interpretListArgs(self, args):
        if ("list" in args):
            if ((len(args["list"]) == 0) or
                (len(args["list"]) == 1 and args["list"][0] == "all")):
                self._listInstr = ["all"]
            else:
                self._listInstr = args["list"]

    def interpretMakeArgs(self, args):
        if ("make" in args):
            self._makeInstr = {}
            if (len(args["make"]) == 0):
                self._makeInstr["vm_aliases"] = ["all"]
                self._makeInstr["instruction"] = ["make"]
            else:
                for i, token in enumerate(args["make"]):
                    #
                    ## --make all
                    if (i == 0 and token == "all" and len(args["make"]) == 1):
                        self._makeInstr["vm_aliases"] = ["all"]
                        self._makeInstr["instruction"] = ["make"]
                    #
                    ## --make fclean (...)
                    elif (i == 0 and token == "fclean"):
                        self._makeInstr["vm_aliases"] = ["all"]
                        self._makeInstr["instruction"] = ["fclean"]
                    #
                    ## --make foo bar baz ...
                    elif (i == 0):
                        self._makeInstr["vm_aliases"] = args["make"]
                        self._makeInstr["instruction"] = ["make"]
                        break

                    #
                    ## --make fclean all
                    elif (i == 1 and token == "all" and args["make"][0] == "fclean"):
                        self._makeInstr["instruction"].append("make")
                        if (len(args["make"]) > 2):
                            self._makeInstr["vm_aliases"] = args["make"][1:]
                    #
                    ## --make fclean (...)
                    elif (i == 1 and args["make"][0] == "fclean"):
                        self._makeInstr["vm_aliases"] = args["make"][1:]
                    #
                    ##
                    elif (i == 1):
                        print("Unrecognized arguments " + args["make"][0] + " " + args["make"][1])
                        exit

    #
    ## Deploy compilation & execution scripts + Qt projects
    def run(self):
        with open(self._infile) as configFile:
            configJson = json.load(configFile)
        guestsVMs = GuestsVMManager(self._verbose, configJson, self._listInstr, self._makeInstr)

        print("Verbose =\t\t" + str(self._verbose))
        print("Infile =\t\t" + self._infile)
        print()

        guestsVMs.run()

        return 0
