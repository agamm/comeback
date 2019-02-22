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
	subprocess.call('code', cwd=options['cwd'], shell=True)