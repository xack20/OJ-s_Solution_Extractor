import sys
import requests as rq
import os
import string
import time
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

clear = lambda: os.system('cls')


HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

s = rq.Session()

dot = "."
msg = "Reconnecting"


def hot(url):
    global msg
    try:
        return s.get(url, headers=HEADERS)

    except:
        if len(msg) == 19:
            print("Reconnecting......./", end='\r')
            time.sleep(.3)
            print("Reconnecting.......-", end='\r')
            time.sleep(.3)
            print("Reconnecting.......\\", end='\r')
            time.sleep(.3)
            print("Reconnecting.......-", end='\r')
            time.sleep(.3)
        else:
            msg += dot
            print(msg, end='\r')
            time.sleep(.5)
        return hot(url)


Email = Password = str()

code_path = os.getcwd()

if sys.platform == 'win32':
    os.chdir("C:\\Users\\" + os.getlogin())

try:
    os.chdir(os.getcwd() + "\\.cache")
    Email, Password = open("login_info.txt").read().splitlines()
    print("\n------->        Logging in from Cache        <--------\n")

except:
    print("\n------->      Login to URI online Judge      <--------\n")

    Email = input("Email    : ")
    Password = input("Password : ")
    if (sys.platform == 'win32' and os.getcwd() == "C:\\Users\\" + os.getlogin()) or (
            sys.platform != 'win32' and os.getcwd() == code_path):
        os.mkdir(".cache")
    os.chdir(os.getcwd() + "\\.cache")
    file = open('login_info.txt', 'w')
    file.write(Email + "\n" + Password)
    file.close()

os.chdir(code_path)
if not os.path.exists("URI Online Judge Solutions"):
    os.mkdir("URI Online Judge Solutions")

origin_path = code_path + "\\URI Online Judge Solutions\\"

origin = "https://www.urionlinejudge.com.br"
url = "https://www.urionlinejudge.com.br/judge/en/login"

r = hot(url)
soup = bs(r.content, 'html.parser')
csrf = soup.find_all('input')[1]['value']

login_data = {
    '_method': "POST",
    "_csrfToken": csrf,
    "email": Email,
    "password": Password,
    "remember_me": 0,
    "_Token[fields]": "41dcc576d590c4d85784392529146d228d160ebf%3A",
    "_Token[unlocked]": ""
}

k = s.post(url, headers=HEADERS, data=login_data)

soup = bs(k.content, 'html.parser')

while soup.find('meta', attrs={"property": "og:title"}).get('content') == "URI Online Judge":
    clear()
    print("\n------->      Invalid Email or Password      <--------")
    print("\n------->              Try Again              <--------\n")
    login_data['email'] = input("Email    : ")
    login_data['password'] = input("Password : ")
    k = s.post(url, headers=HEADERS, data=login_data)
    soup = bs(k.content, 'html.parser')

print("\n\n------->       Successfully Logged in        <--------\n\n")

profile_link = soup.find_all('a')[0]['href']

profile_response = hot(origin + profile_link)
soup = bs(profile_response.content, 'html.parser')

# Total Number of pages

total_page = 0

for dv in soup.find_all('div'):
    if dv.get('id') == 'table-info':
        total_page = int(dv.get_text().split()[2])
        break

extension = {
    'C++': '.cpp',
    'C++17': '.cpp',
    'C++14': '.cpp',
    'C++11': '.cpp',
    'Java': '.java',
    'Java 8': '.java',
    'Java 9': '.java',
    'C': '.c',
    'Python 3': '.py',
    'Python 3.8': '.py',
    'Python': '.py'
}

pbar = tqdm(total=total_page * 30, desc="Downloading..", bar_format="{l_bar}{bar:20}|[ time left: {remaining} ]")

for num in range(1, total_page + 1):
    page_response = hot(origin + profile_link + "?page=" + str(num))
    soup = bs(page_response.content, 'html.parser')
    tr = soup.find_all('tr')

    for i in range(1, len(tr)):
        pbar.update(1)

        data = tr[i].find_all('td')

        if not len(data[0].get_text()):
            continue

        folder = data[0].get_text().strip() + " - "
        fl = []
        for pn in data[1].get_text().strip():
            if pn not in string.punctuation:
                fl.append(pn)
        folder += "".join(fl)

        try:
            lang = extension[data[4].get_text().strip()]
        except:
            lang = ".txt"

        os.chdir(origin_path)

        if not os.path.exists(folder):
            os.mkdir(folder)

        os.chdir(origin_path + folder)

        if os.path.exists("./" + data[3].get_text().strip() + lang):
            continue

        Url = "https://www.urionlinejudge.com.br/judge/en/runs/code/" + data[3].get_text().strip()
        code = hot(Url)
        text = bs(code.content, 'html.parser').pre.get_text()

        file = open(data[3].get_text().strip() + lang, 'w')
        file.write(text)
        file.close()

pbar.close()
print('\n\n**************        Completed         *****************')
time.sleep(3)