import os, bs4
from datetime import datetime
from selenium import webdriver

APP_DIR = os.path.dirname(os.path.dirname('__filename__'))
LOG_FILE = open('log.txt', 'w')


def get_text(element):
    if element is None:
        return ''
    if type(element) == bs4.element.Tag:
        return element.text or ''
    return str(element) or ''


def print_log(*args, **kwargs):
    current_tm = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{current_tm}]', *args, **kwargs)
    LOG_FILE.write(f'[{current_tm}] ' + ' '.join([arg for arg in args]) + '\n')


class Chrome:
    _chrome_driver = os.path.join(APP_DIR, 'chromedriver')
    _chrome_options = webdriver.ChromeOptions()
    _driver = None

    def __init__(self, headless=False):
        if headless:
            self._chrome_options.add_argument('--headless')
            self._chrome_options.add_argument('--no-sandbox')
            self._chrome_options.add_argument('--disable-dev-shm-usage')
            self._chrome_options.add_argument('--disable-gpu')
        self._chrome_options.add_argument('--window-size=1920x1080')
        self._chrome_options.add_argument('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36')
        self._driver = self.create_driver()

    def create_driver(self):
        driver = webdriver.Chrome(self._chrome_driver, options=self._chrome_options)
        return driver

    def get_driver(self):
        return self._driver
