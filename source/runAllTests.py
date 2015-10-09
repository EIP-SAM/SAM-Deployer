#!/usr/bin/python

import sys, getopt, os
from subprocess import call, PIPE

inputFile = ''
cleanStart = False
cleanEnd = False
nbrError = 0

def displayHelp():
    print 'runAllTests.py -d <inputfile> [--cs] [--ce] [-h]'
    print '-d / --dir => tests location'
    print '--cs => clean start'
    print '--ce => clean exit'
    print '-h / --help => display help'

def init(argv):
    global inputFile
    global cleanStart
    global cleanEnd

    try:
        opts, args = getopt.getopt(argv,"hd:",["dir=", "cs", "ce", "help"])
    except getopt.GetoptError:
        displayHelp()
        sys.exit()
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            displayHelp()
            sys.exit()
        elif opt in ("-d", "--dir"):
            inputFile = arg
        elif opt in ("--cs"):
            cleanStart = True;
        elif opt in ("--ce"):
            cleanEnd = True;

    if inputFile == '':
        displayHelp()
        sys.exit()
    elif os.path.isdir(inputFile) == False or os.path.exists(inputFile) == False:
        print 'Directory does not exists !'
        sys.exit()
    else:
        inputFile = os.path.abspath(inputFile)

def getDirContent(path):
    return os.listdir(path)

def getColoredString(string, color):
    colors = {'red': '41', 'green': '42', 'cyan': '46', 'yellow': '43'}
    coloredString = "\033[" + colors[color] + "m"
    return coloredString + string + "\033[0m";

def performMake():
    global cleanStart

    if cleanStart == True:
        call(["make", "clean"], stdout=PIPE)

    return call(["make"], stdout=PIPE)

def cleanEndCompile(binPath):
    global cleanEnd

    if cleanEnd == True:
        call(["make", "clean"], stdout=PIPE)
        call(["rm", "Makefile"], stdout=PIPE)
        call(["rm", binPath], stdout=PIPE)

def compileAllTest(inputFile, filesList):
    startPath = os.getcwd()
    global nbrError

    for fileName in filesList:
        completePath = inputFile + '/' + fileName
        binPath = completePath + '/' + fileName
        proPath = binPath + '.pro'

        if os.path.isdir(completePath) == False or os.path.exists(completePath) == False:
            continue
        elif os.path.exists(proPath) == False:
            print getColoredString('Missing .pro file in  ' + completePath, "red")
            nbrError += 1
            continue

        os.chdir(completePath)
        qmakeRet = call(["qmake", proPath])
        if qmakeRet != 0:
            print getColoredString("Qmake FAIL in " + completePath, "red")
            os.chdir(startPath)
            nbrError += 1
            continue
        makeRet = performMake()
        if makeRet != 0:
            print getColoredString("Makefile FAIL in " + completePath, "red")
            os.chdir(startPath)
            nbrError += 1
            continue
        binRet = call([binPath])
        if binRet != 0:
            nbrError += 1
            print getColoredString("Tests FAIL in " + completePath, "red")
        else:
            print getColoredString("Tests OK", "green")

        cleanEndCompile(binPath)
        os.chdir(startPath)

        return nbrError


init(sys.argv[1:])
compileAllTest(inputFile, getDirContent(inputFile))

sys.exit(nbrError)
