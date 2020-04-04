import time

from util import Chrome, get_text
from bs4 import BeautifulSoup

driver = Chrome().get_driver()
driver.implicitly_wait(3)

url = 'https://www.acmicpc.net/login'
driver.get(url)

username = ''
while not username:
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    loginbar = soup.find('', class_='loginbar').find_all('li')
    if len(loginbar) > 4:
        username = get_text(loginbar[0])
        break
    print("Waiting for login to BOJ...")
    time.sleep(5)

print("Logined!")

time.sleep(10)
driver.quit()
