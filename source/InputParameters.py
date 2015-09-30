#!/usr/bin/env python3

import argparse

class InputArgumentsParser:
    _parser = None
    _args = None

    def __init__(self):
        self.parse()

    def parse(self):
        self._parser = argparse.ArgumentParser()
        self._parser.add_argument("-v", "--verbose",
                            help = "increase output verbosity",
                            action = "store_true")
        self._parser.add_argument("-i", "--infile",
                            help = "use a special configuration file")
        self._parser.add_argument("-l", "--list",
                            nargs = "*",
                            help = "list the available virtual environments")
        self._parser.add_argument("-m", "--make",
                            nargs = "*",
                            help = "provides commands similar to a UNIX Makefiles")
        self._args = self._parser.parse_args()

    def getArguments(self):
        args = {}

        if self._args.verbose:
            args.update({"verbose" : True})
        if self._args.infile:
            args.update({"infile" : self._args.infile})
        if (self._args.list != None):
            args.update({"list" : self._args.list})
        if (self._args.make != None):
            args.update({"make" : self._args.make})

        return args
