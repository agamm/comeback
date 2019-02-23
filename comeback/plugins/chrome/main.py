import os
import subprocess
from comeback import utils


def cb_test():
    """
        Test if we can use this plugin
    """
    # platform = utils.get_platform()
    # try:
    # 	if platform == "windows":
    # 		subprocess.call(["chrome --help"])
    # 	elif platform == "linux":

    # 	elif platform == "mac":

    # except OSError as e:
    # 	return False
    return True


def cb_start(options):
    platform = utils.get_platform()
    if platform == "windows":
        utils.open(["cmd", "/c", "start chrome {}".format(options["url"])])
    elif platform == "linux":
        pass
    elif platform == "mac":
        pass
# cwd = os.path.expanduser(options['cwd'])
# subprocess.call('code {cmd}'.format(cmd=cwd), shell=True)
# start chrome "site1.com"
