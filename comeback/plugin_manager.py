import importlib
from types import ModuleType
from typing import Any, Dict

import click

from comeback import plugins
from comeback.utils import verbose_echo


def call(module: ModuleType,
         **plugin_params: Dict[str, Any]) -> None:
    try:
        success, err = module.run_plugin(**plugin_params)
    except TypeError as e:
        success, err = False, str(e)

    if not success:
        click.echo(
            'There was a problem executing the plugin' +
            f' {module.__name__}: {err}')
        exit(-1)

    verbose_echo(f'Successfully started {module.__name__}!')


def does_exists(plugin_name: str) -> bool:
    all_plugins = plugins.__all__
    is_plugin_found = plugin_name in all_plugins
    if not is_plugin_found:
        click.echo(f'Installed plugins: {", ".join(all_plugins)}')
        click.echo(f'Unknown plugin: {plugin_name}')
    return is_plugin_found


def load(plugin_name: str) -> ModuleType:
    if not plugin_name:
        click.echo(f'Can\'t load a plugin without a plugin name')
        exit(1)

    importer = f'{plugins.__name__}.{plugin_name}.main'
    return importlib.import_module(importer)
