import pytest

from comeback import utils
from tests import test_helper

def test_is_binary_exists():
    assert(utils.is_binary_exists('thisdoesntexistihope') is False)

    if utils.get_platform() == "windows":
        assert(utils.is_binary_exists('python.exe') is True)

def test_is_module_exists():
    assert(utils.is_module_exists('nomoduleinthisname') is False)
    assert(utils.is_module_exists('sys') is True)


def test_read_file(tmp_path):
    # Test no parameter
    with pytest.raises(Exception) as e_info:
        utils.read_file('')

    # Create a dummy file
    test_content = 'content'
    test_file = test_helper.create_test_file(tmp_path, test_content)

    # Acctual test
    result_content = utils.read_file(test_file)
    assert (result_content == test_content)


def test_report_issue():
    exptected_string = 'Report an issue please?' + \
                       ' ( https://github.com/agamm/comeback/issues )'
    assert utils.report_issue() == exptected_string
