import os

import pytest
from click.testing import CliRunner
import comeback.main as main
import pathlib
from comeback import paths
from tests import test_helper


def create_tmp_env_xdg(is_data=True):
    path = '.testxdgdata' if is_data else '.testxdgconfig'
    test_xdg_path = pathlib.Path.home() / path
    backup_data = os.getenv('XDG_DATA_HOME')
    backup_config = os.getenv('XDG_CONFIG_HOME')

    if is_data:
        os.environ['XDG_DATA_HOME'] = str(test_xdg_path)
    else:
        os.environ['XDG_CONFIG_HOME'] = str(test_xdg_path)
    return test_xdg_path, backup_data, backup_config


def restore_env_xdg(data_value, config_value):
    os.environ['XDG_DATA_HOME'] = data_value or ''
    os.environ['XDG_CONFIG_HOME'] = config_value or ''


def test_get_dir_name_type():
    with pytest.raises(ValueError):
        paths.get_dirname('no_kind')

    dir_name = paths.get_dirname('data')
    assert (isinstance(dir_name, pathlib.Path))

    dir_name = paths.get_dirname('config')
    assert (isinstance(dir_name, pathlib.Path))


def test_get_dir_name_env():
    # Test change in env var
    test_xdg_data_path, dv, cv = create_tmp_env_xdg(is_data=True)
    dir_name = paths.get_dirname('data')
    assert (str(dir_name) == str(test_xdg_data_path))
    restore_env_xdg(dv, cv)


def test_get_config_path():
    test_xdg_path, dv, cv = create_tmp_env_xdg(is_data=False)
    config_path = paths.get_config_path()
    assert (str(config_path) == str(test_xdg_path))
    restore_env_xdg(dv, cv)


def test_get_data_path():
    test_xdg_path, dv, cv = create_tmp_env_xdg(is_data=True)
    config_path = paths.get_data_path()
    assert (str(config_path) == str(test_xdg_path))
    restore_env_xdg(dv, cv)