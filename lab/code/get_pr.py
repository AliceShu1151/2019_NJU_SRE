# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 10:30:32 2019

@author: 11515
"""
import os
import requests
from bs4 import BeautifulSoup

pr_num = 1230
url = 'https://github.com/JetBrains/intellij-community/pull/'
path = '../data/pr_title.txt'


def get_pr():
    f = open(path, "w")
    for pr_no in range(0, pr_num):
        # get pr_html
        pr_url = url + str(pr_no)
        r = requests.get(pr_url)
        
        # if requests.get success,  status_code == 200
        if r.status_code != 200:
            continue
        else:
            soup = BeautifulSoup(r.text, features="lxml")
            pr_title = soup.find_all('span', class_="js-issue-title")[0].string.strip()
            print(pr_no, pr_title)
            try:
                txt = str(pr_no)+' '+pr_title+'\n'
                f.write(txt)
            except UnicodeEncodeError:
                f.write(str(pr_no)+' '+'UnicodeEncodeError')
                print('UnicodeEncodeError!')
    f.close()

if __name__ == '__main__':
    if os.path.exists(path) == False:
        get_pr()