# BOJ source saver

![Python application](https://github.com/joonas-yoon/boj-source-saver/workflows/Python%20application/badge.svg)

Save your ACCEPTED codes on [BOJ](https://www.acmicpc.net)

## Requirements

- Chrome WebDriver
- Python 3
- pip

### Chrome WebDriver

Download `chromedriver.exe` from https://sites.google.com/a/chromium.org/chromedriver/downloads

and place it in project directory.

## Set up

(optional) create virutal environment for python if you need

Install python packages:
```
$ pip install -r requirements.txt
```

## How to use

Run a command as following:
```
$ python main.py
```

Chrome starts, and it wait for log in website(BOJ).

When you logged in BOJ, this script will get your latest accepted sources for each problems.

Sources are saved in `~/sources` directory with `{problem_id}.{language_extention}`  (e.g. `1000.py`)


## Terms of Use

We do not take disadvantage by running this program. **You are responsible for your own actions**
