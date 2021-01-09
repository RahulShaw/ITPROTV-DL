from __future__ import unicode_literals

import json
import os
import platform
import re
import sys
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm

import baker

if not (sys.version_info.major == 3 and sys.version_info.minor >= 6):
    print("This script requires Python 3.6 or higher!")
    print("You are using Python {}.{}".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)

if len(sys.argv) < 2:
    print("URL not specified")
    print("Usage -> python driver.py URL")
    sys.exit(1)

print("""

8888888 88888888888 8888888b.  8888888b.   .d88888b.     88888888888 888     888 
  888       888     888   Y88b 888   Y88b d88P" "Y88b        888     888     888 
  888       888     888    888 888    888 888     888        888     888     888 
  888       888     888   d88P 888   d88P 888     888        888     Y88b   d88P 
  888       888     8888888P"  8888888P"  888     888        888      Y88b d88P  
  888       888     888        888 T88b   888     888        888       Y88o88P   
  888       888     888        888  T88b  Y88b. .d88P d8b    888        Y888P    
8888888     888     888        888   T88b  "Y88888P"  Y8P    888         Y8P     
                                                                                                                                                                                                                                                                                                                                                                  
""")

url = sys.argv[1]

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 ' \
             'Safari/537.36 '
headers = {
    'User-Agent': user_agent
}

chrome_options = Options()
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-popup-blocking')
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument('--headless')

if platform.system() == 'Linux':
    if os.path.exists("/usr/bin/chromedriver"):
        browser = webdriver.Chrome(executable_path="/usr/bin/chromedriver",
                                   options=chrome_options)
    else:
        print("Chromedriver not found; expected path '/usr/bin/chromedriver'")
        exit(1)
else:
    if os.path.exists("C:/ChromeDriver/chromedriver.exe"):
        browser = webdriver.Chrome(executable_path="C:/ChromeDriver/chromedriver.exe",
                                   options=chrome_options)
    else:
        print("Chromedriver not found; expected path 'C:/ChromeDriver/chromedriver.exe'")
        exit(1)

browser.set_page_load_timeout(10000)
browser.maximize_window()
browser.get("https://app.itpro.tv/login/")
browser.get(url)

print("Executing for " + url)
time.sleep(5)
print('* Trying to log in ... *')

try:
    baker.bake()
    with open('cookies.json') as cookie_file:
        cookies = json.load(cookie_file)
    for cookie in cookies:
        browser.add_cookie(cookie)
except Exception as e:
    browser.close()
    browser.quit()
    raise e

browser.get(url)
time.sleep(5)
html = browser.page_source
parsed_html = BeautifulSoup(html, 'html5lib')

if parsed_html.find(id='topAccountNav') is None:
    browser.close()
    browser.quit()
    raise Exception(' ** Failed to log in. Please renew the "cookies.txt" file. **')
else:
    print(" - Logged in!")

urls = []
lessons = []
lesson_urls = []
lesson_names = []

course_name = re.sub('[?/:\n\t]', '', parsed_html.find('h3', attrs={'class', 'mb-0'}).text)
print("Course name detected as " + course_name)

browser.execute_script("return document.querySelectorAll('.notCurrentTopic').forEach(e => e.click())")

time.sleep(10)

parsed_html = BeautifulSoup(browser.page_source, 'html5lib')

lesson_links = parsed_html.find_all('a', attrs={'class', 'episodeLink'})

for lesson_link in lesson_links:
    lesson_urls.append('https://app.itpro.tv' + lesson_link['href'])

print("Enumerating links and sources ...")


for index, lesson_url in enumerate(lesson_urls):
    browser.get(lesson_url)
    temp_html = browser.page_source
    temp_parsed_html = BeautifulSoup(temp_html, 'html5lib')
    time.sleep(10)
    while True:
        try:
            lessons.append(browser.execute_script("return document.getElementsByTagName('video')[0].src"))
            lesson_names.append(browser.execute_script("return document.querySelector('#courseContentLayer > div > div > div.d-flex.flex-column.flex-lg-row > div.flex-grow-1 > h1').innerText"))
        except Exception:
            continue
        break
    print(f'Progress: {(index + 1)} of {len(lesson_urls)}', end='\r')

directory = os.getcwd() + os.path.sep + re.sub('[?/:\n]', '', course_name)
if not os.path.exists(directory):
    os.mkdir(directory)

browser.close()
browser.quit()
print("Commencing download ...")

for index, lesson in enumerate(lessons, start=0):
    try:
        print(str.format('Downloading: {} ...', lesson_names[index]))
        r = requests.get(lessons[index], headers=headers, stream=True)
        video_file = directory + os.path.sep + str(index + 1) + ". " + re.sub('[?/:\n]', '',
                                                                              lesson_names[index]) + ".mp4"
        total = r.headers.get('content-length')
        if not os.path.exists(video_file) or os.stat(video_file).st_size != int(total):
            with open(video_file, 'wb') as f:
                if total is None:
                    f.write(r.content)
                else:
                    total_size = int(total, 0)
                    block_size = 1024
                    t = tqdm(total=total_size, unit='iB', unit_scale=True)
                    for data in r.iter_content(block_size):
                        t.update(len(data))
                        f.write(data)
                    t.close()
        else:
            print(" - {} exists. Skipping download.".format(lesson_names[index]))
    except Exception as e:
        print(e)

print('\n\033[92m** Downloads completed! **\033[0m\n')
