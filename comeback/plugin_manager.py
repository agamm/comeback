import click
import importlib

from types import ModuleType
from typing import Any, Dict

from comeback import plugins
from comeback.utils import verbose_echo


def call_plugin(module: ModuleType, plugin_name: str,
                **plugin_params: Dict[str, Any]) -> None:
    success = False
    err = None
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


def does_plugin_exists(plugin_name: str) -> bool:
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