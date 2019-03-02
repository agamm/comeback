from typing import Optional
import webbrowser

from comeback import utils


def open_url_with_browser(browser_name: str, url: str) -> bool:
    try:
        browser = webbrowser.get(using=browser_name)
        browser.open_new_tab(url)
        return True
    except webbrowser.Error:
        return False


def check_plugin(url: Optional[str] = None) -> utils.RUN_STATUS:
    """Test if we can use this plugin"""
    if url is None:
        return False, 'url parameter is not set.'

    return True, None


def run_plugin(url: str) -> utils.RUN_STATUS:
    is_startable, err = check_plugin(url)
    if not is_startable:
        return False, err

    browser_names = ['google-chrome', 'chrome']
    success = False

    while browser_names and not success:
        browser_name = browser_names.pop()
        success = open_url_with_browser(browser_name, url)

    if not success:
        webbrowser.open_new_tab(url)

    return True, None

