import time

import pytest
import os

import comeback.main as main
import pathlib
import comeback.config as config


# TODO: See issue: https://github.com/agamm/comeback/issues/43
# def test_create_path_entity():
#     path_entity = config.create_path_entity('test')
#     last_used = int(
#         time.time())  # this may be undeterministic, consider removing
#     assert path_entity == {'test': last_used}
#
#     path_entity = config.create_path_entity(pathlib.Path('testpath'))
#     last_used = int(
#         time.time())  # this may be undeterministic, consider removing
#     assert path_entity == {'testpath': last_used}
#
#
# def test_add_comeback_path():
#     cb_path = pathlib.Path.cwd() / '.comeback'
#     # We didn't touch the file, so we will get an exception
#     with pytest.raises(FileNotFoundError):
#         config.add_comeback_path(cb_path)
#
#     cb_path.touch()
#     config.add_comeback_path(cb_path)
#     assert str(cb_path) in config.get_comeback_paths()
#     os.remove(str(cb_path))
