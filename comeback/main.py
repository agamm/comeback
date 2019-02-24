import importlib
import os
import pathlib
import pkgutil
import sys

import click
import yaml

from comeback import plugins


exit = sys.exit
get_cwd = pathlib.Path.cwd

IS_VERBOSE = False


def verbose_echo(msg):
    if IS_VERBOSE:
        click.echo(msg)


def get_probable_project_name():
    return get_cwd().name


def call_plugin(module, plugin_name, **plugin_params):
    is_startable, err = module.check(**plugin_params)
    if not is_startable:
        click.echo(f"Couldn't use plugin {plugin_name}: {err}")
        exit()
    module.run(**plugin_params)


def is_plugin_exists(plugin_name):
    all_plugins = plugins.__all__
    is_plugin_found = plugin_name in all_plugins
    if not is_plugin_found:
        click.echo(f'Installed plugins: {", ".join(all_plugins)}')
        click.echo(f'Unknown plugin: {plugin_name}')
    return is_plugin_found


def load_plugin(plugin_name, plugin_params):
    importer = f'{plugins.__name__}.{plugin_name}.main'
    m = importlib.import_module(importer)
    call_plugin(m, plugin_name, **plugin_params)


def run_config(config):
    for plugin_name, plugin_params in config.items():
        if not is_plugin_exists(plugin_name):
            exit()

        verbose_echo('Starting {plugin_name}...')
        verbose_echo('\tParams {plugin_params}...')
        
        load_plugin(plugin_name, plugin_params)


def read_config_file(config_path):
    try:
        with open(config_path, 'r') as fd:
            return yaml.load(fd)
    except IOError:
        print(f'Could not read file: {config_path}')
    except yaml.YAMLError as exc:
        click.echo(exc)


def load_config():
    verbose_echo('Loading configuration file form: {cwd}')
    config_path = get_cwd() / '.comeback'
    config = read_config_file(config_path)

    if config is None:
        return None

    run_config(config)


def main():
    probable_project_name = get_probable_project_name()
    click.echo(f'Starting {probable_project_name}\'s comeback...')
    load_config()


@click.command()
@click.option('-i', '--init', default=False, help='Generate a blank .comeback configuration file.')
@click.option('-v', '--verbose', is_flag=True, help='Show more output.')
# @click.option('--conf', default=False, help='Specify a specific .comeback configuration file path')
def cli(init, verbose):
    global IS_VERBOSE
    IS_VERBOSE = verbose

    if init:
        verbose_echo('Creating a blank .comeback configuration file.')
        return

    main()
