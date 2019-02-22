import click
import os
import subprocess 
import yaml

def init_comeback():
	click.echo('Creating a blank .comeback configuration file.')


def get_cwd():
	return os.path.normpath(os.getcwd())


def get_probable_project_name():
	path = get_cwd()
	return path.split(os.sep)[-1]


def load_config():
	click.echo(get_cwd())


def main():
	probable_project_name = get_probable_project_name()
	click.echo('Starting {}\'s comeback...'.format(probable_project_name))
	load_config()

@click.command()
@click.option('--init', default=False, help='Generate a blank .comeback configuration file.')
# @click.option('--conf', default=False, help='Specify a specific .comeback configuration file path')
def cli(init):
	if init:
		init_comeback()
		return

	main()

