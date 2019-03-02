import importlib
import pathlib
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


def run(cmd, wait=False, use_shell=True):
    # Create a detached windows process
    if wait:
        subprocess.run(cmd)
        return

    subprocess.Popen(cmd, shell=use_shell)


def binary_exists(bin_name):
    return which(bin_name) is not None


def is_module_exists(module_name):
    spec = importlib.util.find_spec(module_name)
    return spec is not None


def get_dirs_in_dir(dirpath):
    """Returns 1st level of dirs in a path"""
    p = pathlib.Path(dirpath).glob('*')
    return filter(pathlib.Path.is_dir, p)


def read_file(path):
    """Read a file should be a pathlib Path object"""
    data = ""
    with path.open('r') as f:
        data = f.read()

    return data


def report_issue():
    """Used when errors are really f*cked up"""
    return "report an issue please? \
        ( https://github.com/agamm/comeback/issues )"
