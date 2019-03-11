import os
from comeback import utils
from typing import Optional


def check_plugin(cwd: Optional[str] = None) -> utils.RUN_STATUS:
    """Test if we can use this plugin"""
    if 'cwd' is None:
        return False, 'cwd parameter is not set.'
    if not utils.is_binary_exists('subl'):
        return False, \
            'Sublime not found, please provide sublime_path option'

    return True, None


def run_linux(cwd: str) -> utils.RUN_STATUS:
    utils.run(['subl', cwd], use_shell=False)
    return True, 'Found sublime'


def run_windows(cwd: str) -> utils.RUN_STATUS:
    subl_path = '\"\"C:\\Programm Files\\Sublime Text 3\\subl.exe\"\"'
    os.system(subl_path)
    return True, 'Found sublime'


def run_plugin(cwd: Optional[str] = None) -> utils.RUN_STATUS:
    is_startable, err = check_plugin(cwd)
    if not is_startable:
        return False, err
    assert cwd is not None
    platform = utils.get_platform()
    if platform == 'windows':
        return run_windows(cwd)
    elif platform == "linux":
        return run_linux(cwd)
