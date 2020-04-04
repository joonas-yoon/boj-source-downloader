import time

from bs4 import BeautifulSoup
from util import Chrome, get_text

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


driver.get(f'https://www.acmicpc.net/user/{username}')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
solved_problems = soup.find_all('span', class_='problem_number')
solved_pids = [get_text(pid) for pid in solved_problems]
for pid in solved_pids:
    driver.get(f'https://www.acmicpc.net/status?problem_id={pid}&user_id={username}&result_id=4&from_mine=1')
    time.sleep(10)
print(' '.join(solved_pids))


time.sleep(10)
driver.quit()
