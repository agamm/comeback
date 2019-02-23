import os
import subprocess
from comeback import utils


def cb_test(options):
    """
        Test if we can use this plugin
    """
    if 'cwd' not in options:
        return False, 'URL parameter is not set.'

    if not utils.binary_exists("code"):
        return False, 'vscode is not installed.'

    return True, None


def cb_start(options):
    cwd = os.path.expanduser(options['cwd'])
    subprocess.call('code {cmd}'.format(cmd=cwd), shell=True)
