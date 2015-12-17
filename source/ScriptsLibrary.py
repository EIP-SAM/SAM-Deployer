import os

class ScriptsLibrary:
    _scriptsLibraryDir = os.path.dirname(os.path.realpath(__file__)) + "/scripts_library"

    scripts = {
        "mount_shared_folder" : _scriptsLibraryDir + "/mount_shared_folder.py",
        "unmount_shared_folder" : _scriptsLibraryDir + "/unmount_shared_folder.py",

        "get_guest_ip_address" : _scriptsLibraryDir + "/get_guest_ip_address.py",
        "get_host_ip_address" : _scriptsLibraryDir + "/get_host_ip_address.py",
        "wait_for_host_ip" : _scriptsLibraryDir + "/wait_for_host_ip.py",

        "make_project" : _scriptsLibraryDir + "/make_project.py"
    }
