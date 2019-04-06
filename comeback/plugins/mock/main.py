import pathlib
import subprocess
import sys
from typing import Optional

from comeback import utils


def check_plugin(print: Optional[str] = None) -> utils.RUN_STATUS:
    """Test if we can use this plugin"""
    if print is None:
        return False, 'cwd parameter is not set.'
    return True, None


def run_plugin(print: Optional[str] = None) -> utils.RUN_STATUS:
    directory = pathlib.Path(print).expanduser()
    r = subprocess.check_output(f'echo {directory}', shell=False)
    sys.stdout.write(str(r))
    if print == "test":
        return False, 'we got a test string'
    return True, None
