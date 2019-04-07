import importlib
import pathlib
import sys
from types import ModuleType
from typing import Any, Dict, Optional, Tuple, List

import click
import yaml

from comeback import config
from comeback import paths
from comeback import plugins

exit = sys.exit

IS_VERBOSE = False


def verbose_echo(msg: str) -> None:
    if IS_VERBOSE:
        click.echo(msg)


def get_probable_project_name() -> str:
    return paths.CURRENT_DIR.name


def parse_args(args: Optional[str] = None) -> Dict[str, str]:
    if not args:
        return {}

    parsed_args = {}
    for arg in args.split(','):
        key_value = arg.split('=')
        if len(key_value) < 2:
            raise ValueError(
                'There was no assignment supplied to args' +
                ' (ie should look like param=value,param2=value2')
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
        exit(1)

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
            return yaml.safe_load(fd)
    except IOError as e:
        click.echo(f'Could not read file {config_path} because {e}')
    except yaml.YAMLError as exc:
        click.echo("YAML Error: " + str(exc))
    return None


def get_config_path() -> pathlib.Path:
    cwd_path = paths.CURRENT_DIR / '.comeback'
    if cwd_path.exists():
        config.add_comeback_path(cwd_path)
        return cwd_path

    last_comeback_used = config.get_last_comeback()

    verbose_echo('No .comeback file found in the current directory, ' +
                 f'starting last session found ({last_comeback_used})')
    return last_comeback_used


def load_config(config_path: Optional[pathlib.Path] = None) -> None:
    verbose_echo(f'Loading configuration file form: {paths.CURRENT_DIR}')
    if not config_path:
        config_path = get_config_path()

    config = read_config_file(config_path)

    if config is None:
        verbose_echo(
            'Error: no .comeback file found in the current directory nor in ' +
            'previous sessions.')
        return None

    run_config(config)


def create_comeback_file_here() -> pathlib.Path:
    verbose_echo('Creating a blank .comeback configuration file.')
    path = paths.CURRENT_DIR / '.comeback'
    if path.exists():
        verbose_echo('.comeback file already exists here. Will only touch it.')
    path.touch()
    config.add_comeback_path(path)
    return path


def main() -> None:
    probable_project_name = get_probable_project_name()
    click.echo(f'Starting {probable_project_name}\'s comeback...')
    load_config()


def get_last_used() -> List[Dict[str, Any]]:
    last_used_list = []
    for last_used_path in config.get_recent_comebacks(5):
        path, last_used = last_used_path
        last_used_list.append({'path': path, 'last_used': last_used})

    return sorted(last_used_list, key=lambda k: k['last_used'],
                  reverse=True)


def list_last_used() -> Tuple[List[Dict[str, Any]], str]:
    sorted_last_used = get_last_used()
    sorted_last_str = ""
    for index, recipe in enumerate(sorted_last_used):
        sorted_last_str += f'{index + 1} - {recipe["path"]} \n'

    return sorted_last_used, sorted_last_str


def choose_last_used() -> None:
    click.echo('Please choose one of the following .comeback recipes:')
    last_used, last_used_str = list_last_used()
    click.echo(last_used_str)
    index = int(input("> "))  # pragma: no cover
    path = last_used[index - 1]['path']  # pragma: no cover
    load_config(path)  # pragma: no cover
    config.add_comeback_path(path)  # pragma: no cover


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('-i', '--init', is_flag=True, default=False,
              help='Generate a blank .comeback configuration file.')
@click.option('-v', '--verbose', is_flag=True, help='Show more output.')
@click.option('-l', '--last_used', is_flag=True, help='Show recently used' +
                                                      '.comeback recipes.')
def cli(ctx: click.Context, init: bool, verbose: bool, last_used: bool) \
        -> None:
    global IS_VERBOSE
    IS_VERBOSE = verbose

    if ctx.invoked_subcommand is not None:
        verbose_echo('Invoking subcommand: %s' % ctx.invoked_subcommand)
        return

    if init:
        create_comeback_file_here()
        return

    if last_used:
        choose_last_used()
        return  # pragma: no cover

    main()


@cli.command()
@click.argument('plugin', required=True)
@click.argument('plugin_params', required=False)
def run(plugin: str, plugin_params: str) -> None:
    verbose_echo(f'Running plugins: {plugin} with args: {plugin_params}')
    load_plugin(plugin, parse_args(plugin_params))
