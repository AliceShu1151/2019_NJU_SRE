# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 10:30:32 2019

@author: jss
"""
import re,csv
import requests
from bs4 import BeautifulSoup

url = 'https://bugs.eclipse.org/bugs/show_bug.cgi?id='
path = '../data/eclipse_bugs_'


def get_bug(bug_no):
    bug_url = url + str(bug_no)

    status_code = 201
    while status_code != 200:
        try:
            r = requests.get(bug_url,timeout=5)
            status_code = r.status_code
        except:
            print('timeout! retry...')
            
    # if requests.get success,  status_code == 200
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, features="lxml")
        if soup.find_all('div', attrs={'class':"throw_error",'id':"error_msg"}) != []:
            print(str(bug_no)+' You must enter a valid bug number!')
            return None
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
        
        reported = soup.find_all('td', attrs={'id':"bz_show_bug_column_2"})[0]
        bug['reported'] = reported.contents[1].contents[1].find_all('td')[0].text.replace('\n','').strip()
        
        modified = soup.find_all('td', attrs={'id':"bz_show_bug_column_2"})[0]
        modified = modified.contents[1].contents[3].find_all('td')[0].text.replace('\n','').strip()
        bug['modified'] = re.sub('\\(.*?\\)','',modified).strip()
        
        cclist = soup.find_all('td', attrs={'id':"bz_show_bug_column_2"})[0]
        cclist = cclist.contents[1].contents[5].find_all('td')[0].text.replace('\n','').strip()
        bug['cclist'] = ' '.join(re.sub('\\(.*?\\)','',cclist).strip().split()[0:2])
        
        return bug
    else:
        return None
        

if __name__ == '__main__':
    start = 10000
    end = start + 10000
    i_path = path + str(start) + '.csv'
    with open(i_path, 'a+', errors='ignore') as f:
        f_csv = csv.writer(f,lineterminator='\n')
        for bug_no in range(start,end):  #552850
            bug_info = get_bug(bug_no)
    
            if bug_no == start:                    
                f_csv.writerow(bug_info.keys())
                
            if bug_info != None:                    
                f_csv.writerow(bug_info.values())
                print(bug_no, bug_info['title'])
                    
        f.close()
            