from sys import platform as _platform
import subprocess 

def get_platform():
	if _platform.startswith("linux"):
	   return "linux"
	elif _platform == "darwin":
	   return "mac"
	elif _platform.startswith("win"):
	   return "windows"
	return "other"

def open(cmd):
	subprocess.Popen(cmd, shell=False, stdin=None, stdout=None, stderr=None, close_fds=True)