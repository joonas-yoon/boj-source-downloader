import os, sys, bs4
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.common import exceptions

APP_DIR = os.path.dirname(os.path.dirname('__filename__'))
LOG_FILE = open('log.txt', 'w')


def get_text(element):
    if element is None:
        return ''
    if type(element) == bs4.element.Tag:
        return element.text or ''
    return str(element) or ''


def print_log(*args, **kwargs):
    cur_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'[{cur_time}]', *args, **kwargs)
    args_str = ' '.join([str(arg) for arg in args])
    LOG_FILE.write(f'[{cur_time}] {args_str}\n')


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
        self._chrome_options.add_argument('--window-size=1600,900')
        self._chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36')
        self._driver = self.create_driver()

    def create_driver(self):
        driver = webdriver.Chrome(self._chrome_driver, options=self._chrome_options)
        driver.implicitly_wait(3)
        return driver

    def get_driver(self):
        return self._driver
    
    def get(self, url):
        self.handle_exceptions()
        self._driver.get(url)
        
    def parse_html(self):
        self.handle_exceptions()
        html = self._driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        return soup
    
    def handle_exceptions(self):
        try:
            _ = self._driver.window_handles
        except (exceptions.WebDriverException, exceptions.NoSuchWindowException) as e:
            print_log('[ERROR]', e, file=sys.stderr)
            self._driver.quit()
            raise SystemExit
            sys.exit(0)
        return False