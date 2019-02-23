import os
import subprocess
from comeback import utils


def cb_test(options):
    """
        Test if we can use this plugin
    """
    if 'url' not in options:
        return False, 'URL parameter is not set.'

    if not utils.module_exists('webbrowser'):
        return False, 'webbrowser module doesn\'t exist!'

    return True, None


def cb_start(options):
    import webbrowser
    new = 2  # open in a new tab
    try:
        webbrowser.get(using='google-chrome').open(options['url'], new=new)
    except webbrowser.Error:
        pass

    # Try to open again, and if it doesn't work open the default
    try:
        webbrowser.get(using='chrome').open(options['url'], new=new)
    except webbrowser.Error:
        webbrowser.open(options['url'], new=new)

