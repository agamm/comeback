import pytest

from comeback import utils


def test_report_issue():
    exptected_string = 'Report an issue please?' + \
            ' ( https://github.com/agamm/comeback/issues )'
    assert utils.report_issue() == exptected_string
