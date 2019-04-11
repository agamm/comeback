import pytest
from click.testing import CliRunner
import comeback.main as main
import pathlib

from comeback import plugin_manager


def test_help_message():
    # Should show the help message
    runner = CliRunner()
    result = runner.invoke(main.cli, ['--help'])
    assert result.exit_code == 0
    assert 'Usage: ' in result.output
    assert '-i, --init' in result.output
    assert '-v, --verbose' in result.output
    assert '-l, --last_used' in result.output
    assert '--help' in result.output


def test_parse_args():
    assert main.parse_args() == {}
    assert main.parse_args('a=123') == {'a': '123'}
    assert main.parse_args('a=123,b=321') == {'a': '123', 'b': '321'}
    with pytest.raises(ValueError):
        assert main.parse_args(',') == {}
        assert main.parse_args(',,') == {}
        assert main.parse_args(',=') == {}
        assert main.parse_args('a=321,=') == {}


def test_no_comeback():
    # Should try to open a local .comeback recipe and fail
    runner = CliRunner()
    result = runner.invoke(main.cli)
    assert result.exit_code == 0
    assert 'Starting ' in result.output


def test_no_comeback_verbose():
    # Should try to open a local .comeback recipe and fail verbosely
    runner = CliRunner()
    result = runner.invoke(main.cli, ['-v'])
    assert result.exit_code == 0
    assert 'Starting ' in result.output
    assert 'Loading recipe ululation file from' in result.output
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
    assert result.exit_code == 0
    assert pathlib.Path('./.comeback').is_file()

    # Remove the file, as we don't really need it anymore (poor child)
    pathlib.Path('./.comeback').unlink()


def test_does_plugin_exists():
    assert plugin_manager.does_plugin_exists('mock')
    assert not plugin_manager.does_plugin_exists('__NOPLUGINNAMEDLIKETHIS__')


# TODO: See issue: https://github.com/agamm/comeback/issues/43
# def test_call_plugin():
#     runner = CliRunner()
#     result = runner.invoke(main.run, ['mock', 'value=321'])
#     assert result.exit_code == 0
#     assert '321' in result.stdout
#
#     with pytest.raises(ModuleNotFoundError):
#         runner.invoke(main.run, ['__NOPLUGINNAMEDLIKETHIS__', 'r=312'],
#                       catch_exceptions=False)
#
#     result = runner.invoke(main.run, ['mock', 'notvalue=312'])
#     assert result.exit_code == 0
#     assert "unexpected keyword argument 'notprint'" in result.output
#
#     result = runner.invoke(main.run, ['mock'])
#     assert result.exit_code == 0
#     assert 'expected str' in result.output
#
#     result = runner.invoke(main.run, ['mock', 'value=test'])
#     assert result.exit_code == 0
#     assert 'we got a test string' in result.stdout
#
#     result = runner.invoke(main.run, [])
#     assert result.exit_code == 2
#     assert 'Missing argument 'PLUGIN'' in result.stdout
#
#
# def test_comeback_file_mock(tmp_path):
#     runner = CliRunner()
#     with runner.isolated_filesystem():
#         paths.CURRENT_DIR = pathlib.Path(os.getcwd())  # Fixes the isolated fs
#         with open('.comeback', 'w') as f:
#             yaml.dump({'mock': {'value': 'wowow'}}, f,
#                       default_flow_style=False)
#
#         result = runner.invoke(main.cli, '-v')
#         assert result.exit_code == 0
#         assert 'Successfully' in result.stdout
#         assert 'b'wowow\\n'' in result.stdout
#
#
# def test_comeback_file_noplugin(tmp_path):
#     runner = CliRunner()
#     with runner.isolated_filesystem():
#         paths.CURRENT_DIR = pathlib.Path(os.getcwd())  # Fixes the isolated fs
#         with open('.comeback', 'w') as f:
#             yaml.dump({'__NOPLUGINNAMEDLIKETHIS__': {'value': 'wowow'}}, f,
#                       default_flow_style=False)
#
#         result = runner.invoke(main.cli, '-v')
#         assert result.exit_code == 0
#         assert 'Unknown plugin' in result.stdout
#
#
# def test_comeback_file_bad_yaml(tmp_path):
#     runner = CliRunner()
#     with runner.isolated_filesystem():
#         paths.CURRENT_DIR = pathlib.Path(os.getcwd())  # Fixes the isolated fs
#         with open('.comeback', 'w') as f:
#             f.write('p:\n231\n')
#
#         result = runner.invoke(main.cli, '-v')
#         assert result.exit_code == 0
#         assert 'YAML Error' in result.output
#
#
# def test_comeback_file_already_exists_comeback_file(tmp_path):
#     runner = CliRunner()
#     with runner.isolated_filesystem():
#         paths.CURRENT_DIR = pathlib.Path(os.getcwd())  # Fixes the isolated fs
#         with open('.comeback', 'w') as f:
#             yaml.dump({'mock': {'value': 'wowow'}}, f,
#                       default_flow_style=False)
#
#         result = runner.invoke(main.cli, '-v --init')
#         assert result.exit_code == 0
#         assert 'file already exists here' in result.stdout
#
#
# def test_comeback_subcommand(tmp_path):
#     runner = CliRunner()
#
#     result = runner.invoke(main.cli, ['-v', 'run', 'mock', 'value=123'])
#     assert result.exit_code == 0
#     assert 'Invoking subcommand' in result.output
#     assert 'b'123\\n'' in result.stdout
