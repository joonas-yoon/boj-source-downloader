import os
from selenium import webdriver
from util import Chrome, APP_DIR


def test_chrome():
    chrome_driver = os.path.join(APP_DIR, 'chromedriver')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(chrome_driver, options=chrome_options)
    driver.implicitly_wait(3)
    assert driver is not None

    driver.quit()


def test_chrome_util():
    chrome = Chrome(headless=True)
    driver = chrome.get_driver()
    assert driver is not None
    driver.quit()