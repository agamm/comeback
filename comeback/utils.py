from sys import platform as _platform
import subprocess
import importlib


def get_platform():
    if _platform.startswith("linux"):
        return "linux"
    elif _platform == "darwin":
        return "mac"
    elif _platform.startswith("win"):
        return "windows"
    return "other"


def open(cmd):
    subprocess.Popen(cmd, shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)

def binary_exists(bin_name):
    from shutil import which
    return which(bin_name) is not None


def module_exists(module_name):
    spec = importlib.util.find_spec(module_name)
    return spec is not None
