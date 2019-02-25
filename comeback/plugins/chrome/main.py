import webbrowser

def open_url_with_browser(browser_name, url):
    try:
        browser = webbrowser.get(using=browser_name)
        browser.open_new_tab(url)
        return True
    except webbrowser.Error:
        return False


def check_plugin(url=None):
    """Test if we can use this plugin"""
    if url is None:
        return False, 'url parameter is not set.'

    return True, None


def run_plugin(url):
    browser_names = ['google-chrome', 'chrome']
    success = False

    while browser_names and not success:
        browser_name = browser_names.pop()
        success = open_url_with_browser(browser_name, url)

    if not success:
        webbrowser.open_new_tab(url)

    return True, None
