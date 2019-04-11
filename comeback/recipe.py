import json
import click
import pathlib

from typing import Any, Dict, Optional, List
from comeback import paths
from comeback import config
from comeback.plugins import manager
from comeback.utils import verbose_echo

RECIPE_FILENAME = ".comeback"


def read_file(recipe_path: pathlib.Path) -> Optional[Dict[str, Any]]:
    try:
        with open(recipe_path, 'r') as fd:
            return json.load(fd)
    except IOError as e:
        click.echo(f'Could not read file {recipe_path} because {e}')
    except json.JSONDecodeError as exc:
        click.echo('JSON Error: ' + str(exc))
    return None


def run(recipe: List[Dict[str, Any]]) -> None:
    for plugin_dict in recipe:
        for plugin_name, plugin_params in plugin_dict.items():
            if not manager.does_exists(plugin_name):
                exit()

            verbose_echo(f'Starting {plugin_name}...')
            verbose_echo(f'\tParams {plugin_params}...')

            plugin = manager.load(plugin_name)
            manager.call(plugin, **plugin_params)


def create_file() -> pathlib.Path:
    verbose_echo('Creating a blank .comeback configuration file.')
    path = paths.CURRENT_DIR / RECIPE_FILENAME
    if path.exists():
        verbose_echo('.comeback file already exists here. Will only touch it.')
    path.touch()
    config.add_comeback_path(path)
    return path


def get_path() -> pathlib.Path:
    cwd_path = paths.CURRENT_DIR / RECIPE_FILENAME
    if cwd_path.exists():
        config.add_comeback_path(cwd_path)
        return cwd_path

    last_comeback_used = config.get_last_comeback()

    verbose_echo('No .comeback file found in the current directory, ' +
                 f'starting last session found ({last_comeback_used})')
    return last_comeback_used


def load(recipe_path: Optional[pathlib.Path] = None) -> None:
    verbose_echo(f'Loading recipe ululation file from: {paths.CURRENT_DIR}')
    if not recipe_path:
        recipe_path = get_path()

    recipe = read_file(recipe_path)

    if recipe is None:
        verbose_echo(
            'Error: no .comeback file found in the current directory nor in ' +
            'previous sessions.')
        return None

    run(recipe)
