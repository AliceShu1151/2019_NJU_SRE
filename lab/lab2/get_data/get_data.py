# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 10:30:32 2019

@author: 11515
"""
import os,re,csv
import requests
from bs4 import BeautifulSoup

url = 'https://bugs.eclipse.org/bugs/show_bug.cgi?id='
path = '../data/eclipse_bugs.csv'


def get_bug(bug_no):
    bug_url = url + str(bug_no)
    r = requests.get(bug_url)
        
    # if requests.get success,  status_code == 200
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, features="lxml")
        bug = {}
        bug['id'] = bug_no
        bug['title'] = soup.find_all('span', attrs={'id':"short_desc_nonedit_display"})[0].text.strip()
        bug['status'] = ' '.join(soup.find_all('span', attrs={'id':"static_bug_status"})[0].text.replace('\n','').split())
        
        alias = soup.find_all('th', attrs={'id':"field_label_alias"})[0]
        bug['alias'] = alias.findNext('td').string.strip()
        
        product = soup.find_all('th', attrs={'id':"field_label_product"})[0]
        bug['product']= product.findNext('td').string.strip()
               
        component = soup.find_all('td', attrs={'id':"field_container_component"})[0].text.replace('\n','')
        bug['component'] = re.sub('\\(.*?\\)','',component).strip()
        
        version = soup.find_all('th', attrs={'id':"field_label_version"})[0]
        bug['version'] = ' '.join(version.findNext('td').text.split()[:])
        
        importance = soup.find_all('th', attrs={'class':"field_label",'id':""})[1]
        importance = ' '.join(importance.findNext('td').text.replace('\n','').split())
        bug['importance'] = re.sub('\\(.*?\\)','',importance).strip()
        
        target_milestone = soup.find_all('th', attrs={'id':"field_label_target_milestone"})[0]
        bug['target_milestone'] = ' '.join(target_milestone.findNext('td').text.split()[:])
        
        assignee = soup.find_all('th', attrs={'id':"field_label_assigned_to"})[0]
        bug['assignee'] = assignee.findNext('td').text.replace('\n','').strip()
        
        qa_contact = soup.find_all('th', attrs={'id':"field_label_qa_contact"})[0]
        bug['qa_contact'] = qa_contact.findNext('td').text.replace('\n','').strip()
        
        bug_attr_url = soup.find_all('th', attrs={'id':"field_label_bug_file_loc"})[0]
        bug['url'] = bug_attr_url.findNext('td').text.replace('\n','').strip()
        
        whiteboard = soup.find_all('th', attrs={'id':"field_label_status_whiteboard"})[0]
        bug['whiteboard'] = whiteboard.findNext('td').text.replace('\n','').strip()
        
        keywords = soup.find_all('th', attrs={'id':"field_label_keywords"})[0]
        bug['keywords'] = keywords.findNext('td').text.replace('\n','').strip()
        
        depends_on = soup.find_all('th', attrs={'id':"field_label_dependson"})[0]
        bug['depends_on'] = depends_on.findNext('td').text.replace('\n','').strip()
        
        blocks = soup.find_all('th', attrs={'id':"field_label_blocked"})[0]
        bug['blocks'] = blocks.findNext('td').text.replace('\n','').strip()
        
        return bug
    else:
        return None
        

if __name__ == '__main__':
    if os.path.exists(path) == False:
        with open(path, 'w') as f:
            f_csv = csv.writer(f,lineterminator='\n')
            for bug_no in range(1,101):  
                bug_info = get_bug(bug_no)
        
                if bug_no == 1:                    
                    f_csv.writerow(bug_info.keys())
                
                f_csv.writerow(bug_info.values())
                
                print(bug_no, bug_info['title'])
            f.close()
            