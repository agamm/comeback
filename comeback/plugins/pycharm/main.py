import pathlib
from typing import Optional

from comeback import utils


def check_plugin(cwd: Optional[str] = None) -> utils.RUN_STATUS:
    """Test if we can use this plugin"""
    if cwd is None:
        return False, 'cwd parameter is not set.'
    return True, None


def run_windows(cwd: str) -> utils.RUN_STATUS:
    home = pathlib.Path.home()
    pycharm_settings_dirs = list(home.glob('*pycharm*'))

    if not pycharm_settings_dirs or len(pycharm_settings_dirs) == 0:
        return False, 'pycharm\'s settings dir was not found.'

    pycharm_settings_dir = pycharm_settings_dirs[0]
    # I really hate how JetBrains are forcing me to puke
    home_settings_file = pycharm_settings_dir.joinpath('system', '.home')
    if not home_settings_file.exists():
        return False, 'pycharm\'s settings .home file was not found.'

    install_path = utils.read_file(home_settings_file)
    pycharm_install_path = pathlib.Path(install_path)
    if not pycharm_install_path.exists():
        return False, (f'pycharm\'s install path from the settings'
                        'file is not correct, {utils.report_issue()}')

    # I actually checked and the pycharm.exe is 32bit,
    #  let's only use it if the 64 is not found
    pycharm_exe32 = pycharm_install_path.joinpath('bin', 'pycharm.exe')
    pycharm_exe64 = pycharm_install_path.joinpath('bin', 'pycharm64.exe')

    pyc32 = pycharm_exe32.exists()
    pyc64 = pycharm_exe64.exists()

    if not pyc32 and pyc64:
        return False, 'pycharm\'s exe files are not found.'
    elif pyc64:
        utils.run([str(pycharm_exe64), str(cwd)], use_shell=False, detach=False)
    else:
        utils.run([str(pycharm_exe64), str(cwd)], use_shell=False, detach=False)

    return True, 'Found pycharm'


def run_linux(cwd: str, pycharm_path: Optional[str]) -> utils.RUN_STATUS:
    if not utils.is_binary_exists('pycharm-community'):
        if not pycharm_path:
            return (False,
                    'PyCharm not found, please provide pycharm_path option')
        utils.run([pycharm_path, cwd], use_shell=False)
        return True, 'Found pycharm'

    utils.run(['pycharm-community', cwd], use_shell=False)
    return True, 'Found pycharm'


def run_mac(cwd: str) -> utils.RUN_STATUS:
    apps_path = pathlib.Path('/Applications')
    pycharm_dir_pattern = '*[Pp]y[Cc]harm*'
    results = list(apps_path.glob(pycharm_dir_pattern))
    if not results:
        return False, "Can't find PyCharm in Applications, did you install it?"

    pycharm_path = str(results[0])
    utils.run(f'open "{pycharm_path}" --args {cwd}', use_shell=True)
    return True, 'Found pycharm'


def run_plugin(cwd: Optional[str],
               pycharm_path: Optional[str] = None) -> utils.RUN_STATUS:
    is_startable, err = check_plugin(cwd)
    if not is_startable:
        return False, err
    assert isinstance(cwd, str)

    cwd = pathlib.Path(cwd).expanduser()
    platform = utils.get_platform()
    if platform == 'windows':
        return run_windows(cwd)
    elif platform == 'linux':
        return run_linux(cwd, pycharm_path)
    elif platform == 'mac':
        return run_mac(cwd)

    return False, 'Failed to identify your OS'
