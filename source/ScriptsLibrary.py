import os

class ScriptsLibrary:
    _scriptsLibraryDir = os.path.dirname(os.path.realpath(__file__)) + "/scripts_library"
    _linuxScriptsDir = _scriptsLibraryDir + "/linux_guest"
    _windowsScriptsDir = _scriptsLibraryDir + "/windows_guest"

    scripts = {

        "linux" : {
            "mount_shared_folder" : _linuxScriptsDir + "/mount_shared_folder.bash",
            "unmount_shared_folder" : _linuxScriptsDir + "/unmount_shared_folder.bash",
        },

        "windows" : {
            "mount_shared_folder" : _windowsScriptsDir + "/mount_shared_folder.bat",
            "unmount_shared_folder" : _windowsScriptsDir + "/unmount_shared_folder.bat",
        }
    }
