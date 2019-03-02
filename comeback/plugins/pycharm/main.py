import pathlib
from comeback import utils


def check_plugin(cwd=None):
    """Test if we can use this plugin"""
    if 'cwd' is None:
        return False, 'cwd parameter is not set.'
    return True, None


def run_windows(cwd):
    home = pathlib.Path.home()
    pycharm_settings_dir = list(home.glob('*pycharm*'))

    if not pycharm_settings_dir or len(pycharm_settings_dir) == 0:
        return False, "pycharm's settings dir was not found."

    pycharm_settings_dir = pycharm_settings_dir[0]
    # I really hate how JetBrains are forcing me to puke
    home_settings_file = pycharm_settings_dir.joinpath("system", ".home")
    if not home_settings_file.exists():
        return False, "pycharm's settings .home file was not found."

    install_path = utils.read_file(home_settings_file)
    pycharm_install_path = pathlib.Path(install_path)
    if not pycharm_install_path.exists():
        return False, f"pycharm's install path from the settings \
            file is not correct, {utils.report_issue()}"

    # I actually checked and the pycharm.exe is 32bit,
    #  let's only use it if the 64 is not found
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


def run_mac(cwd):
    apps_path = pathlib.Path('/Applications')
    apps = list(apps_path.glob("*"))
    results = list(filter(lambda x: "pycharm" in x.name.lower(), apps))
    if len(results) == 0:
        return False, "Didn't find pycharm in applications, did you install it?"

    pycharm_path = str(results[0])
    utils.run(f"open {pycharm_path} {cwd}")
    return True, "Found pycharm"

def run_plugin(cwd):
    is_startable, err = check_plugin(cwd)
    if not is_startable:
        return False, err

    platform = utils.get_platform()
    if platform == "windows":
        return run_windows(cwd)
    elif platform == "linux":
        pass
    elif platform == "mac":
        run_mac(cwd)
