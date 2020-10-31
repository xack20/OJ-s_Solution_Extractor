import os
import time
import random
import requests as rq
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

ts = time.time()

session = rq.Session()

login_url = "https://codeforces.com/enter"

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
}

login_page = session.get(login_url, headers=HEADERS)

csrf = bs(login_page.content, 'html.parser').find("meta", attrs={"name": "X-Csrf-Token"}).get('content')
cf_handle = "Zakaria_Foysal"
password = "ilove3.1416"

login_data = {
    "csrf_token": csrf,
    "action": "enter",
    "ftaa": "7xngp4ost1oilaxroc",
    "bfaa": "32ccf174a9c28597ea662cf9c615e2af",
    "handleOrEmail": cf_handle,
    "password": password,
    "remember": "on",
    "_tta": "252"
}

session.post(login_url, data=login_data, headers=HEADERS)


def site_hit(URL,t):
    if t > 5:
        return
    try:
        time.sleep(random.random()+t)
        return bs(session.get(URL, headers=HEADERS).content, 'html.parser').pre.get_text()
    except:
        return site_hit(URL,t+.2)


data = session.get('https://codeforces.com/api/user.status?handle=' + cf_handle + '&from=1&count=50000').json()

if data['status'] != "OK":
    print("Invalid Username")
    exit()

data = list(data['result'])

fdt = []
for dt in data:
    if dt['verdict'] == 'OK':
        fdt.append(dt)
data = fdt

if not os.path.exists('CF_Solutions'):
    os.mkdir('CF_Solutions')

origin_folder = os.getcwd() + os.path.sep + 'CF_Solutions'
os.chdir(origin_folder)

print()
pbar = tqdm(total=len(data), desc="Downloading..", bar_format="{l_bar}{bar:20}| [ time left: {remaining} ]")

while len(data):

    dt = data.pop()

    problem_index = dt['problem']['index']
    problem_name = dt['problem']['name']
    problem_tags = dt['problem']['tags']
    contest_id = dt['problem']['contestId']

    programmingLanguage = dt['programmingLanguage']
    submission_id = dt['id']

    if not os.path.exists(str(contest_id)):
        os.mkdir(str(contest_id))

    os.chdir(os.getcwd() + os.path.sep + str(contest_id))

    if not os.path.exists(problem_index):
        os.mkdir(problem_index)

    os.chdir(os.getcwd() + os.path.sep + problem_index)

    url = "https://codeforces.com/contest/" + str(contest_id) + "/submission/" + str(submission_id)

    if not os.path.exists("./" + str(submission_id) + ".txt"):

        code = ""
        
        for itr in range(3):
            code = site_hit(url,0.0)
            if code:
                break

        if not code:
            data.append(dt)
            random.shuffle(data)
            os.chdir(origin_folder)
            continue
        
        file = open(str(submission_id) + ".txt", 'w')
        file.write(str(code))
        file.close()
        
    pbar.update(1)

    os.chdir(origin_folder)

pbar.close()


print("\nSuccessfully Downloaded!")


te = time.time()

print("\nTime taken :", time.strftime("%H:%M:%S", time.gmtime(te - ts)))
input("\nPress any key to continue")
