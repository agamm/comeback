import importlib
import pathlib
import platform
from shutil import which
import subprocess
from typing import Iterator, Optional, Tuple


RUN_STATUS = Tuple[bool, Optional[str]]


def get_platform() -> str:
    platforms = {
        'Linux': 'linux',
        'Windows': 'windows',
        'Darwin': 'mac',
    }

    return platforms.get(platform.system(), 'other')


def run(cmd: str, wait: bool = False) -> None:
    # Create a detached windows process
    if wait:
        subprocess.run(cmd)

        return

    subprocess.Popen(cmd, shell=False)


def binary_exists(bin_name: str) -> bool:
    return which(bin_name) is not None


def is_module_exists(module_name: str) -> bool:
    spec = importlib.util.find_spec(module_name)
    return spec is not None


def get_dirs_in_dir(dirpath: str) -> Iterator[pathlib.Path]:
    """Returns 1st level of dirs in a path"""
    all_files = pathlib.Path(dirpath).glob('*')
    return filter(pathlib.Path.is_dir, all_files)


def read_file(path: pathlib.Path) -> str:
    """Read a file should be a pathlib Path object"""
    data = ""
    with path.open('r') as f:
        data = f.read()

    return data


def report_issue() -> str:
    """Used when errors are really f*cked up"""
    return 'report an issue please? \
        ( https://github.com/agamm/comeback/issues )'
