import importlib
import platform
from shutil import which
import subprocess
from pathlib import Path


def get_platform():
    platforms = {
        'Linux': 'linux',
        'Windows': 'windows',
        'Darwin': 'mac',
    }

    return platforms.get(platform.system(), 'other')


def run(cmd, wait=False):
    # Create a detached windows process
    if wait:
        subprocess.run(cmd)

        return

    subprocess.Popen(cmd, shell=False)


def binary_exists(bin_name):
    return which(bin_name) is not None


def is_module_exists(module_name):
    spec = importlib.util.find_spec(module_name)
    return spec is not None


def get_dirs_in_dir(dirpath):
    p = Path(dirpath).glob('*')
    return [x for x in p if x.is_dir()]


def read_file(path):
    """Read a file should be a pathlib Path object"""
    data = ""
    with path.open('r') as f:
        data = f.read()

    return data


def report_issue():
    """Used when errors are really f*cked up"""
    return "report an issue please? ( https://github.com/agamm/comeback/issues )"
