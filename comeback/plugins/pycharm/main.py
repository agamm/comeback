import os
import pathlib
import subprocess

from comeback import utils


def check_plugin(cwd=None):
    """Test if we can use this plugin"""
    if 'cwd' is None:
        return False, 'cwd parameter is not set.'
    return True, None


def run_windows(cwd):
    home_dir = os.path.expanduser('~')
    wdirs = utils.get_dirs_in_dir(home_dir)
    pycharm_settings_dir = None

    for i, v in enumerate(wdirs):
        if 'pycharm' in v.name.lower():
            pycharm_settings_dir = v

    if not pycharm_settings_dir:
        return False, "pycharm's settings dir was not found."

    # I really hate how JetBrains are forcing me to puke
    home_settings_file = pycharm_settings_dir.joinpath("system", ".home")
    if not home_settings_file.exists():
        return False, "pycharm's settings .home file was not found."

    install_path = utils.read_file(home_settings_file)
    pycharm_install_path = pathlib.Path(install_path)
    if not pycharm_install_path.exists():
        return False, f"pycharm's install path from the settings file is not correct, {utils.report_issue()}"

    # I actually checked and the pycharm.exe is 32bit, let's only use it if the 64 is not found
    pycharm_exe32 = pycharm_install_path.joinpath("bin", "pycharm.exe")
    pycharm_exe64 = pycharm_install_path.joinpath("bin", "pycharm64.exe")

    pyc32 = pycharm_exe32.exists()
    pyc64 = pycharm_exe64.exists()

    if not pyc32 and pyc64:
        return False, "pycharm's exe files are not found."
    elif pyc64:
        utils.run(f"{pycharm_exe64} {cwd}")
    else:
        utils.run(f"{pycharm_exe64} {cwd}")

    return True, "Found pycharm"


def run_plugin(cwd):
    platform = utils.get_platform()
    if platform == "windows":
        return run_windows(cwd)
    elif platform == "linux":
        pass  # @TODO
    elif platform == "mac":
        pass  # @TODO
