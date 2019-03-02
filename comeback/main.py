import importlib
import pathlib
import sys
from types import ModuleType
from typing import Any, Dict, Optional

import click
import yaml

from comeback import plugins


exit = sys.exit
get_cwd = pathlib.Path.cwd

IS_VERBOSE = False


def verbose_echo(msg: str) -> None:
    if IS_VERBOSE:
        click.echo(msg)


def get_probable_project_name() -> str:
    return get_cwd().name


def parse_args(args: Optional[str]) -> Dict[str, str]:
    if not args:
        return {}

    parsed_args = {}
    for arg in args.split(","):
        key_value = arg.split("=")
        parsed_args[key_value[0]] = key_value[1]

    return parsed_args


def call_plugin(module: ModuleType, plugin_name: str,
                **plugin_params: Dict[str, Any]) -> None:
    try:
        success, err = module.run_plugin(**plugin_params)
    except TypeError as e:
        click.echo(
            f'There was a problem executing the plugin {plugin_name}: {e}')
        exit()

    if not success:
        click.echo(
            f'There was a problem executing the plugin {plugin_name}: {err}')
        exit()

    verbose_echo(f'Successfully started {plugin_name}!')


def is_plugin_exists(plugin_name: str) -> bool:
    all_plugins = plugins.__all__
    is_plugin_found = plugin_name in all_plugins
    if not is_plugin_found:
        click.echo(f'Installed plugins: {", ".join(all_plugins)}')
        click.echo(f'Unknown plugin: {plugin_name}')
    return is_plugin_found


def load_plugin(plugin_name: str, plugin_params: Dict[str, Any]) -> None:
    if not plugin_name:
        click.echo(f'Can\'t load a plugin without a plugin name')
        exit()

    # Fix plugins that don't require params
    if not plugin_params:
        plugin_params = {}

    importer = f'{plugins.__name__}.{plugin_name}.main'
    m = importlib.import_module(importer)
    call_plugin(m, plugin_name, **plugin_params)


def run_config(config: Dict[str, Any]) -> None:
    for plugin_name, plugin_params in config.items():
        if not is_plugin_exists(plugin_name):
            exit()

        verbose_echo(f'Starting {plugin_name}...')
        verbose_echo(f'\tParams {plugin_params}...')

        load_plugin(plugin_name, plugin_params)


def read_config_file(config_path: pathlib.Path) -> Optional[Dict[str, Any]]:
    try:
        with open(config_path, 'r') as fd:
            return yaml.load(fd)
    except IOError as e:
        click.echo(f'Could not read file {config_path} because {e}')
    except yaml.YAMLError as exc:
        click.echo(exc)
    return None


def load_config() -> None:
    verbose_echo(f'Loading configuration file form: {get_cwd()}')
    config_path = get_cwd() / '.comeback'
    config = read_config_file(config_path)

    if config is None:
        return None

    run_config(config)


def main() -> None:
    probable_project_name = get_probable_project_name()
    click.echo(f'Starting {probable_project_name}\'s comeback...')
    load_config()


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('-i', '--init', default=False, help='Generate a blank \
    .comeback configuration file.')
@click.option('-v', '--verbose', is_flag=True, help='Show more output.')
def cli(ctx: click.Context, init: bool, verbose: bool) -> None:
    global IS_VERBOSE
    IS_VERBOSE = verbose

    if ctx.invoked_subcommand is not None:
        verbose_echo('Invoking subcommand: %s' % ctx.invoked_subcommand)
        return

    if init:
        verbose_echo('Creating a blank .comeback configuration file.')
        get_cwd().joinpath('.comeback').touch()
        return

    main()


@cli.command()
@click.argument('plugin', required=True)
@click.argument('plugin_params', required=False)
def run(plugin: str, plugin_params: str) -> None:
    verbose_echo(f'Running plugins: {plugin} with args: {plugin_params}')
    load_plugin(plugin, parse_args(plugin_params))
