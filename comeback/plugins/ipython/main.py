import pathlib
from typing import List, Optional, Set

from comeback import utils


def get_bad_modules(module_names: List[str]) -> Set[str]:
    unique_module_names = set(module_names)
    valid_modules = set(filter(utils.is_module_exists, unique_module_names))
    bad_modules = unique_module_names - valid_modules
    return bad_modules


def check_plugin(module_names: List[str]) -> utils.RUN_STATUS:
    """Test if we can use this plugin"""
    if utils.is_binary_exists('ipython') is None:
        return False, 'IPython was not found.'
    bad_modules = get_bad_modules(module_names)
    if bad_modules:
        return False, f'Can\'t find modules: {bad_modules}.'
    return True, None

def get_launch_command(module_names: List[str]) -> str:
    imports = ''.join(f'import {module};' for module in module_names)
    command = f'ipython -c "{imports}" -i'
    return command


def run_plugin(modules: List[str]) -> utils.RUN_STATUS:
    is_startable, err = check_plugin(modules)
    if not is_startable:
        return False, err

    ipython_cmd = get_launch_command(modules)
    utils.run(ipython_cmd)
    return True, None
