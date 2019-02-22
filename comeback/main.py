import click
import os, sys
import yaml
from . import plugins
import pkgutil
import importlib

def exit():
	sys.exit()

def init_comeback(verbose):
	if verbose:
		click.echo('Creating a blank .comeback configuration file.')


def get_cwd():
	return os.path.normpath(os.getcwd())


def get_probable_project_name():
	path = get_cwd()
	return path.split(os.sep)[-1]


def get_installed_plugins():
	return [name for _, name, _ in pkgutil.iter_modules(plugins.__path__)]


def call_plugin(module, app_name, app_params):
	# if not module.cb_test():
	# 	click.echo("Cloudn't use plugin {}".format(app_name))
	# 	exit()
	module.cb_start(app_params)


def run_config(config):
	for app_name, app_params in config.items():
		
		if app_name not in get_installed_plugins():
			print(get_installed_plugins())
			click.echo("No plugin found for {}".format(app_name))
			exit()

		click.echo("Starting {}...".format(app_name))
		click.echo("\tParams {}...".format(app_params))

		# Iterate all the plugins and choose the correct one
		for importer, name, _ in pkgutil.iter_modules(plugins.__path__):
			if name != app_name:
				continue
			m = importlib.import_module(plugins.__name__ + '.' + name + '.main')
			call_plugin(m, app_name, app_params)
			break




def load_config(verbose):
	cwd = get_cwd()
	if verbose:
		click.echo('Loading configuration file form: {}'.format(cwd))

	conf_path = os.path.join(cwd, ".comeback")
	with open(conf_path, 'r') as fd:
		try:
			run_config(yaml.load(fd))
		except yaml.YAMLError as exc:
			click.echo(exc)


def main(verbose):
	probable_project_name = get_probable_project_name()
	click.echo('Starting {}\'s comeback...'.format(probable_project_name))
	load_config(verbose)

@click.command()
@click.option('-i', '--init', default=False, help='Generate a blank .comeback configuration file.')
@click.option('-v', '--verbose', is_flag=True, help='Show more output.')
# @click.option('--conf', default=False, help='Specify a specific .comeback configuration file path')
def cli(init, verbose):
	if init:
		init_comeback(verbose)
		return

	main(verbose)

