import os
import subprocess 


def cb_test():
	"""
		Test if we can use this plugin
	"""
	try:
		subprocess.call(["code --help"])
	except OSError as e:
		return False


def cb_start(options):
	print(options)
	cwd = os.path.expanduser(options['cwd'])
	subprocess.call('code {cmd}'.format(cmd=cwd), shell=True)