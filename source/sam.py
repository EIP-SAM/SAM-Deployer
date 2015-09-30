#!/usr/bin/env python3

from Deployer import *
from InputParameters import *

def main():
    #
    ## Get command line arguments
    argsParser = InputArgumentsParser()
    inputArgs = argsParser.getArguments()

    #
    ## Launch deployer
    deployer = Deployer(inputArgs)
    return deployer.run()

ret = main()
exit(ret)
