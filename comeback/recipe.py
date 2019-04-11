import json
import pathlib
from typing import Any, Dict, Optional, List

import click

from comeback import config, plugin_manager
from comeback import paths
from comeback.utils import verbose_echo


FILENAME = '.comeback'


def read_file(recipe_path: pathlib.Path) -> Optional[Dict[str, Any]]:
    try:
        with open(recipe_path, 'r') as fd:
            return json.load(fd)
    except IOError as e:
        click.echo(f'Could not read file {recipe_path} because {e}')
    except json.JSONDecodeError as exc:
        click.echo('JSON Error: ' + str(exc))
    return None


def run_step(step_dict):
    for plugin_name, plugin_params in step_dict.items():
        if not plugin_manager.does_exists(plugin_name):
            exit(-1)

        verbose_echo(f'Starting {plugin_name}...')
        verbose_echo(f'\tParams {plugin_params}...')

        plugin = plugin_manager.load(plugin_name)
        plugin_manager.call(plugin, **plugin_params)


def run(recipe: List[Dict[str, Any]]) -> None:
    for step_dict in recipe:
        run_step(step_dict)


def create() -> pathlib.Path:
    verbose_echo('Creating a blank .comeback configuration file.')
    path = paths.CURRENT_DIR / FILENAME
    if path.exists():
        verbose_echo('.comeback file already exists here. Will only touch it.')
    path.touch()
    config.add_comeback_path(path)
    return path


def get_path() -> pathlib.Path:
    cwd_path = paths.CURRENT_DIR / FILENAME
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
