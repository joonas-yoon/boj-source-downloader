import os, time
import meta
from os.path import isfile, join
from random import random
from util import Chrome, get_text, print_log

SOURCE_DIR = os.path.join('sources')
if not os.path.isdir(SOURCE_DIR):
    os.mkdir(SOURCE_DIR)
source_files = [f for f in os.listdir(SOURCE_DIR) if isfile(join(SOURCE_DIR, f))]
saved_pids = set([os.path.splitext(f)[0] for f in source_files])


# return: username
def get_login(chrome):
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

    print_log(f'Logged in! Hello, {username}')
    return username


# return IDs of solved problems
def get_solved_problems(chrome, username):
    chrome.get(f'https://www.acmicpc.net/user/{username}')
    soup = chrome.parse_html()
    solved_problems = soup.find_all('span', class_='problem_number')
    solved_pids = [get_text(pid) for pid in solved_problems]
    return solved_pids


# List of accepted submissions
def get_submissions(chrome, username, problem_id):
    chrome.get(f'https://www.acmicpc.net/status?problem_id={problem_id}&user_id={username}&result_id=4&from_mine=1')

    # Get latest submission id
    soup = chrome.parse_html()
    submissions = soup.find(id='status-table').find_all('tr')
    subs = []
    for sub in submissions:
        sub_id = sub.get('id')
        if sub_id:
            subs.append(sub_id.replace('solution-', ''))
    return subs


def get_source(chrome, submission_id):
    # Get page of latest source
    chrome.get(f'https://www.acmicpc.net/source/{submission_id}')
    try:
        # Get a code
        soup = chrome.parse_html()
        source = '\n'.join([get_text(line) for line in soup.find_all('pre', class_='CodeMirror-line')])

        # Detect file extension
        table = soup.find('table', class_='table')
        language_name = get_text(table.find_all('tr')[1].find_all('td')[7])
    except Exception as e:
        return None

    return {
        'language': language_name,
        'source': source
    }


def detect_extension(language_name):
    detect_failed = not language_name in meta.LANGUAGE_EXTENSION
    extension = 'unknown'
    if not detect_failed:
        extension = meta.LANGUAGE_EXTENSION[language_name]
        detect_failed = not extension
    if detect_failed:
        print_log(f'[Warn] Can not detected ext of {language_name}. it saved as .unknown')
        extension = 'unknown'
    return extension


# Save as file
def save_source(problem_id, language_name, source):
    # Save as file
    extension = detect_extension(language_name)
    source_file = f'{problem_id}.{extension}'
    with open(os.path.join(SOURCE_DIR, source_file), 'w', encoding='utf-8') as f:
        f.write(source)


# Main process
def run(chrome):
    username = get_login(chrome)
    solved_pids = get_solved_problems(chrome, username)

    for current in range(len(solved_pids)):
        problem_id = solved_pids[current]
        if problem_id in saved_pids:
            print_log(f'Skipped Problem {problem_id} (reason: already saved)')
            continue

        sub_id = get_submissions(chrome, username, problem_id)[0]
        source = get_source(chrome, sub_id)
        if source:
            language_name = source['language']
            save_source(problem_id, language_name, source['source'])
            # Print log of process
            print_log(f'Saved Problem {problem_id} Submission #{sub_id} ({language_name}) ({current + 1}/{len(solved_pids)})')
        else:
            print_log(f'FAILED Problem {problem_id} Submission #{sub_id}')
            raise Exception

        time.sleep(random() * 2 + .5)


if __name__ == '__main__':
    print_log(f'Build...')
    chrome = Chrome()
    print_log(f'Start downloading...')
    while True:
        try:
            run(chrome)
        except Exception as e:
            print_log('[ERROR]', e)
            continue
        break
    print_log(f'Finished!')
    time.sleep(10)
    chrome.quit()
