import os
import pathlib
import subprocess

from comeback import utils


def check_plugin(cwd=None):
    """Test if we can use this plugin"""
    if 'cwd' is None:
        return False, 'cwd parameter is not set.'

    if not utils.binary_exists('code'):
        return False, 'vscode is not installed.'

    return True, None


def run_plugin(cwd):
    directory = pathlib.Path(cwd).expanduser()
    subprocess.call(f'code {directory}', shell=True)
    return True, None
