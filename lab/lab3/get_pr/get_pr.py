# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 15:30:28 2019

@author: 11515
"""

import csv
import requests
from bs4 import BeautifulSoup

url = 'https://github.com/JetBrains/intellij-community/pull/'
path = '../data/pr_id.csv'

def get_discuss(path, pr_id):
    with open(path.replace('id',str(pr_id)), "w", errors='ignore', newline='') as f:   
        pr_url = url + str(pr_id)
        r = requests.get(pr_url)
        csv_writer = csv.writer(f)
#         if requests.get success,  status_code == 200
        if r.status_code != 200:
            return
        else:
            soup = BeautifulSoup(r.text, features="lxml")
            pr_title = soup.find_all('span', class_="js-issue-title")[0].string.strip()
            print(pr_id, pr_title)
            try:
                csv_writer.writerow([pr_id,pr_title])
            except UnicodeEncodeError:
                f.write(str(pr_id)+' '+'UnicodeEncodeError')
                print('UnicodeEncodeError!')
            blocks = soup.find_all('table', class_="d-block")
            for block in blocks:
                lines = block.find_all('p')
                time = block.find_previous('relative-time').get('datetime')
                for line in lines:
                    if line.parent.name == 'blockquote':
                        continue
                    else:
                        try:
                            csv_writer.writerow([time,'discuss',line.text])
                        except UnicodeEncodeError:
                            f.write(str(pr_id)+' '+'UnicodeEncodeError')
                            print('UnicodeEncodeError!')    
    f.close()
    
def get_commit(path, pr_id):
    with open(path.replace('id',str(pr_id)), "a+", errors='ignore', newline='') as f:   
        pr_url = url + str(pr_id) + '/commits'
        r = requests.get(pr_url)
        csv_writer = csv.writer(f)
#         if requests.get success,  status_code == 200
        if r.status_code != 200:
            return
        else:
            soup = BeautifulSoup(r.text, features="lxml")
            commit = soup.find_all('div', class_="commit-group-title")
            if len(commit) != 0:
                commit = commit[0]
                commits = commit.find_next_siblings('ol')
                for block in commits:
                    lines = block.find_all('li')
                    for one in lines:
                        text = one.find_all('a', class_="message js-navigation-open")
                        if len(text) == 0:
                            text = 'None'
                        else:
                            text = text[0].text
#                        auth = one.find_all('a', class_="commit-author tooltipped tooltipped-s user-mention")[0].text
                        time = one.find_all('relative-time')[0].get('datetime')
                        link = 'github.com'+one.find_all('a', class_="sha btn btn-outline BtnGroup-item")[0].get('href')
                        try:
                            csv_writer.writerow([time,'commit',text,link])
                        except UnicodeEncodeError:
                            f.write(str(pr_id)+' '+'UnicodeEncodeError')
                            print('UnicodeEncodeError!')  
    f.close()

def get_pr(pr_id):
    get_discuss(path, pr_id)
    get_commit(path, pr_id)

if __name__ == '__main__':
    for pr_id in range(865,900):
        pr_url = url + str(pr_id)
        r = requests.get(pr_url)
        if r.status_code == 200:
            get_pr(pr_id)
    print("Congratulations!")