import os
import pathlib
from typing import NamedTuple

from comeback import recipe

# The XDG is a standard that helps declutter the user's home directory
# from configuration and data files.
# https://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html


class XdgPath(NamedTuple):
    name: str
    xdg_variable_name: str
    default_dir: pathlib.Path


HOMEDIR = pathlib.Path.home()
PATH_KINDS = {
    'data': XdgPath('data', 'XDG_DATA_HOME', HOMEDIR / '.local' / 'share'),
    'config': XdgPath('config', 'XDG_CONFIG_HOME', HOMEDIR / '.config'),
}


def get_dirname(kind: str) -> pathlib.Path:
    if kind not in PATH_KINDS:
        raise ValueError(f'No such kind: {kind}. Use {PATH_KINDS.keys()})')
    _, xdg_variable_name, fallback_dir = PATH_KINDS[kind]
    directory_path = os.getenv(xdg_variable_name, default=fallback_dir)
    return pathlib.Path(directory_path)


def get_path(kind: str, filename: str = '') -> pathlib.Path:
    fullpath = get_dirname(kind)
    fullpath.mkdir(parents=True, exist_ok=True)
    fullpath = fullpath.joinpath(filename)
    return fullpath


def get_config_path(**kwargs: str) -> pathlib.Path:
    return get_path('config', **kwargs)


def get_data_path(**kwargs: str) -> pathlib.Path:
    return get_path('data', **kwargs)


def get_default_comeback_file_path() -> pathlib.Path:
    return pathlib.Path.home() / recipe.FILENAME


DEFAULT_COMEBACK_FILE = get_default_comeback_file_path()
DATA_DIR = get_data_path()
CONFIG_DIR = get_config_path()
PATHS_DATA_FILE = get_data_path(filename='paths')
CURRENT_DIR = pathlib.Path.cwd()
