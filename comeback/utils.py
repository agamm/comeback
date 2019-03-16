import importlib
import pathlib
import platform
import shlex
import subprocess
from shutil import which
from typing import Any, Dict, List, Optional, Tuple, Union


RUN_STATUS = Tuple[bool, Optional[str]]
CMD_PARAMS = Union[List[str], str]


def get_platform() -> str:
    platforms = {
        'Linux': 'linux',
        'Windows': 'windows',
        'Darwin': 'mac',
    }

    return platforms.get(platform.system(), 'other')


def _format_command(cmd: CMD_PARAMS) -> List[str]:
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    assert isinstance(cmd, list)
    return cmd


def _get_detach_flags() -> Dict[str, Any]:
    kwargs = {}
    if get_platform() == 'windows':
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        DETACHED_PROCESS = 0x00000008
        kwargs['creationflags'] = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
    else:
        kwargs['start_new_session'] = True
    return kwargs


def run(cmd: CMD_PARAMS, use_shell: bool = False, detach: bool = True) -> None:
    cmd = _format_command(cmd)

    kwargs = {}
    if detach:
        kwargs.update(_get_detach_flags())

    subprocess.Popen(cmd, shell=use_shell, **kwargs)


def is_binary_exists(bin_name: str) -> bool:
    return which(bin_name) is not None


def is_module_exists(module_name: str) -> bool:
    spec = importlib.util.find_spec(module_name)
    return spec is not None


def read_file(path: pathlib.Path) -> str:
    """Read a file should be a pathlib Path object"""
    data = ''
    with path.open('r') as f:
        data = f.read()

    return data


def report_issue() -> str:
    """Used when errors are really f*cked up"""
    return ('Report an issue please? '
            '( https://github.com/agamm/comeback/issues )')
