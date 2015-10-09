# SAM-Deployer
Code deployer/tester for multiple OS environments

## Description

The first purpose of this software is to compile and execute tests for our [SAM-Solution](https://github.com/EIP-SAM/SAM-Solution) project

This software is designed to be used with Qt/C++/QML projects  
It actually uses VMware Workstation and pre-configured virtual machines to work


## Usage

```
usage: sam.py [-h] [-v] [-i INFILE] [-l [LIST [LIST ...]]]
              [-m [MAKE [MAKE ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -i INFILE, --infile INFILE
                        use a special configuration file
  -l [LIST [LIST ...]], --list [LIST [LIST ...]]
                        list the available virtual environments
  -m [MAKE [MAKE ...]], --make [MAKE [MAKE ...]]
                        provides commands similar to a UNIX Makefiles
```

### `--make` available options

```
--make
--make all
--make fclean
--make fclean all
--make vm_alias_1 vm_alias_2 # ...
--make fclean vm_alias_1 vm_alias_2 # ...
```

## Configuration file

Uses JSON format

The default configuration file is named `sam-deployer.json` and is supposed to be placed in the current directory  
It is also possible to input a custom configuration file via `--infile` or `-i ` command line arguments

Both *Unix* and *Windows* path style are valid, depending on the OS used
```
"/home/foo/bar/vm_alias_1.vmx",
"C:\Foo\Bar\vm_alias_1.vmx"
```

### A valid example

```json
{
    "vm-paths" :
    [
        "/home/foo/bar/vm_alias_1.vmx",
        "/home/foo/bar/vm_alias_2.vmx",
    ]
}
```

## Tests script

The source/runAllTests.py file is a python script used for perform all tests in SAM Solution project.

For that, the script takes at least one argument : ./runAllTests.py -d sam_solution/source/tests

With the mandatory parameter `-d`, the script can find all tests in the target directory.

There is a couple of other usefull optional parameters :

 `--cs` : perform a `make clean` before compiling each test.

 `--ce` : clean every test directory after each test (rm .o, Makefile and test's binary).

 `-h/--help` : display a reminder of every parameters avaible.