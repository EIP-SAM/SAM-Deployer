import os

class ScriptsLibrary:
    _scriptsLibraryDir = os.path.dirname(os.path.realpath(__file__)) + "/scripts_library"

    scripts = {
        "mount_shared_folder" : _scriptsLibraryDir + "/mount_shared_folder.py",
        "unmount_shared_folder" : _scriptsLibraryDir + "/unmount_shared_folder.py",

        "make_project" : _scriptsLibraryDir + "/make_project.py"
    }
