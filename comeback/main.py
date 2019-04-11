import pathlib
import sys
from typing import Any, Dict, Optional, Tuple, List

import click

from comeback import config, utils
from comeback import paths
from comeback import plugin_manager
from comeback import recipe_manager
from comeback.recipe_manager import RECIPE_FILENAME
from comeback.utils import verbose_echo

exit = sys.exit


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


def get_config_path() -> pathlib.Path:
    cwd_path = paths.CURRENT_DIR / RECIPE_FILENAME
    if cwd_path.exists():
        config.add_comeback_path(cwd_path)
        return cwd_path

    last_comeback_used = config.get_last_comeback()

    verbose_echo('No .comeback file found in the current directory, ' +
                 f'starting last session found ({last_comeback_used})')
    return last_comeback_used


def main() -> None:
    probable_project_name = get_probable_project_name()
    click.echo(f'Starting {probable_project_name}\'s comeback...')
    recipe_manager.load_recipe()


def get_last_used() -> List[Dict[str, Any]]:
    last_used_list = []
    for last_used_path in config.get_recent_comebacks(5):
        path, last_used = last_used_path
        last_used_list.append({'path': path, 'last_used': last_used})

    return sorted(last_used_list, key=lambda k: k['last_used'],
                  reverse=True)


def list_last_used() -> Tuple[List[Dict[str, Any]], str]:
    sorted_last_used = get_last_used()
    sorted_last_str = ''
    for index, recipe in enumerate(sorted_last_used):
        sorted_last_str += f'{index + 1} - {recipe["path"]} \n'

    return sorted_last_used, sorted_last_str


def choose_last_used() -> None:
    click.echo('Please choose one of the following .comeback recipes:')
    last_used, last_used_str = list_last_used()
    click.echo(last_used_str)
    index = int(input('> '))  # pragma: no cover
    path = last_used[index - 1]['path']  # pragma: no cover
    recipe_manager.load_recipe(path)  # pragma: no cover
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
    utils.IS_VERBOSE = verbose

    if ctx.invoked_subcommand is not None:
        verbose_echo('Invoking subcommand: %s' % ctx.invoked_subcommand)
        return

    if init:
        recipe_manager.create_recipe_file()
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
    module = plugin_manager.load_plugin(plugin)
    plugin_manager.call_plugin(module, **parse_args(plugin_params))


if __name__ == '__main__':
    main()
