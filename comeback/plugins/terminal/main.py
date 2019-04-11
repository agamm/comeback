import pathlib
from typing import Optional

from comeback import utils


def check_plugin(cwd: str = None) -> utils.RUN_STATUS:
    """Test if we can use this plugin"""
    if cwd is None:
        return False, 'cwd parameter is not set.'
    if not pathlib.Path(cwd).is_dir():
        return False, 'cwd is not an existing directory'
    return True, None


def run_windows(cwd: str) -> utils.RUN_STATUS:
    pass


def run_linux(cwd: str) -> utils.RUN_STATUS:
    pass


def run_mac(cwd: str) -> utils.RUN_STATUS:
    terminal_type = 'iTerm'
    apps_path = pathlib.Path('/Applications')
    iterm_dir_pattern = '*[iI][tT]erm*'
    results = list(apps_path.glob(iterm_dir_pattern))
    if not results:
        terminal_type = 'Terminal'

    utils.run(f'open -a {terminal_type} {cwd}')

    return True, 'Opened terminal successfully'


def run_plugin(cwd: Optional[str]) -> utils.RUN_STATUS:
    is_startable, err = check_plugin(cwd)
    if not is_startable:
        return False, err

    assert isinstance(cwd, str)

    platform = utils.get_platform()
    if platform == 'windows':
        return run_windows(cwd)
    elif platform == 'linux':
        return run_linux(cwd)
    elif platform == 'mac':
        return run_mac(cwd)
