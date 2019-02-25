import importlib
import platform
from shutil import which
import subprocess


def get_platform():
    platforms = {
        'Linux': 'linux',
        'Windows': 'windows',
        'Darwin': 'mac',
    }

    return platforms.get(platform.system(), 'other')


def run(cmd):
    subprocess.run(cmd)


def binary_exists(bin_name):
    return which(bin_name) is not None


def is_module_exists(module_name):
    spec = importlib.util.find_spec(module_name)
    return spec is not None
