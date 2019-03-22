import pytest
import click
from click.testing import CliRunner
import comeback.main as main

def test_help_message():
    runner = CliRunner()
    result = runner.invoke(main.cli, ['--help'])
    assert (result.exit_code == 0)
    assert ("Usage: " in result.output)
    assert ("-i, --init" in result.output)
    assert ("-v, --verbose" in result.output)
    assert ("-l, --last_used" in result.output)
    assert ("--help" in result.output)