import os, time
import meta
from os.path import isfile, join
from random import random
from util import Chrome, get_text

SOURCE_DIR = os.path.join('sources')
if not os.path.isdir(SOURCE_DIR):
    os.mkdir(SOURCE_DIR)
source_files = [f for f in os.listdir(SOURCE_DIR) if isfile(join(SOURCE_DIR, f))]
saved_pids = set([os.path.splitext(f)[0] for f in source_files])

chrome = Chrome()

chrome.get('https://www.acmicpc.net/login')

username = None
while not username:
    soup = chrome.parse_html()
    loginbar = soup.find('', class_='loginbar').find_all('li')
    if len(loginbar) > 4:
        username = get_text(loginbar[0])
        break
    print('Waiting for login to BOJ...')
    time.sleep(5)

print(f'Logged in! Hello, {username}')


chrome.get(f'https://www.acmicpc.net/user/{username}')
soup = chrome.parse_html()
solved_problems = soup.find_all('span', class_='problem_number')
solved_pids = [get_text(pid) for pid in solved_problems]
n_solved = len(solved_pids)

for current in range(n_solved):
    problem_id = solved_pids[current]
    if problem_id in saved_pids:
        print(f'Skipped Problem {problem_id} (reason: already saved)')
        continue
    
    # List of accepted submissions
    chrome.get(f'https://www.acmicpc.net/status?problem_id={problem_id}&user_id={username}&result_id=4&from_mine=1')

    # Get latest submission id
    soup = chrome.parse_html()
    submissions = soup.find(id='status-table').find_all('tr')
    sub_id = None
    for sub in submissions:
        sub_id = sub.get('id')
        if sub_id:
            sub_id = sub_id.replace('solution-', '')
            break

    if sub_id is None:
        continue

    # Get page of latest source
    chrome.get(f'https://www.acmicpc.net/source/{sub_id}')
    soup = chrome.parse_html()
    source = '\n'.join([get_text(line) for line in soup.find_all('pre', class_='CodeMirror-line')])

    # Detect file extension
    language_name = get_text(soup.find('table', class_='table').find_all('tr')[1].find_all('td')[7])
    detect_failed = not language_name in meta.LANGUAGE_EXTENSION
    if not detect_failed:
        extension = meta.LANGUAGE_EXTENSION[language_name]
        detect_failed = not extension
    if detect_failed:
        print(f'[Warn] Can not detected ext of {language_name}. it saved as .unknown')
        extension = 'unknown'

    # Save as file
    source_file = f'{problem_id}.{extension}'
    with open(os.path.join(SOURCE_DIR, source_file), 'w', encoding='utf-8') as f:
        f.write(source)

    # Print log of process
    print(f'Saved Problem {problem_id} Submission #{sub_id} ({language_name}) ({current}/{n_solved})')

    time.sleep(random() * 2 + .5)


time.sleep(10)
chrome.quit()
