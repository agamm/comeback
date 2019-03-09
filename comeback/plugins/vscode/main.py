import pathlib
import subprocess
from typing import Optional

from comeback import utils


def check_plugin(cwd: Optional[str] = None) -> utils.RUN_STATUS:
    """Test if we can use this plugin"""
    if cwd is None:
        return False, 'cwd parameter is not set.'

    if not utils.is_binary_exists('code'):
        return False, 'vscode is not installed.'

    return True, None


def run_plugin(cwd: Optional[str] = None) -> utils.RUN_STATUS:
    is_startable, err = check_plugin(cwd)
    if not is_startable:
        return False, err
    assert cwd is not None
    directory = pathlib.Path(cwd).expanduser()
    subprocess.call(f'code {directory}', shell=True)
    return True, None
