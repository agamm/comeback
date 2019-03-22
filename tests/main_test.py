import pytest
from click.testing import CliRunner
import comeback.main as main
import pathlib


def test_help_message():
    # Should show the help message
    runner = CliRunner()
    result = runner.invoke(main.cli, ['--help'])
    assert (result.exit_code == 0)
    assert ('Usage: ' in result.output)
    assert ('-i, --init' in result.output)
    assert ('-v, --verbose' in result.output)
    assert ('-l, --last_used' in result.output)
    assert ('--help' in result.output)


def test_no_comeback():
    # Should try to open a local .comeback recipe and fail
    runner = CliRunner()
    result = runner.invoke(main.cli)
    assert (result.exit_code == 0)
    assert ('Starting ' in result.output)


def test_no_comeback_verbose():
    # Should try to open a local .comeback recipe and fail verbosely
    runner = CliRunner()
    result = runner.invoke(main.cli, ['-v'])
    assert (result.exit_code == 0)
    assert ('Starting ' in result.output)
    assert ('Loading configuration file form: ' in result.output)
    assert ('Error: no .comeback file found in the ' +
            'current directory nor in previous sessions.' in result.output)


def test_last_used_displayed():
    # Should show the last used .comeback recipes
    runner = CliRunner()
    result = runner.invoke(main.cli, ['-l'])
    assert (result.exit_code == 1)  # TODO: Make sure this is indeed correct
    assert ('Please choose one of the following .comeback recipes:'
            in result.output)


def test_init():
    # Should create a .comeback file in the current directory
    runner = CliRunner()
    result = runner.invoke(main.cli, ['-i'])
    assert (result.exit_code == 0)
    assert (pathlib.Path("./.comeback").is_file())

    # Remove the file, as we don't really need it anymore (poor child)
    pathlib.Path("./.comeback").unlink()
