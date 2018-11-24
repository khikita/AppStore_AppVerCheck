# coding: UTF-8
import os,sys
import argparse
import urllib2
import requests,json
import filecmp
from bs4 import BeautifulSoup
 
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', type=str, required=True, nargs=1,  help="Store url.")
parser.add_argument('-txt', type=str)
args = parser.parse_args()
url = args.url[0]
outfile = args.txt
 
webhook_url = "https://outlook.office.com/webhook/"
 
 
def updateTxt(txtpath):
    f = open(txtpath,'w')
    f.write(app_version.encode('utf_8') )
    f.close()
 
def teamsPost():
        source = 'がバージョンアップしました'
        strTxt = unicode(source, 'utf-8')
        body = {'text': title + " " + strTxt}
        headers = {'content-type': 'application/json'}
        requests.post(webhook_url,data = json.dumps(body), headers=headers)
 
html = urllib2.urlopen(url)
 
soup = BeautifulSoup(html,"html.parser")
 
title = soup.title.string
p_tag = soup.find_all("time")
 
app_version = ""
 
for tag in p_tag:
        try:
                string_ = tag.get("class").pop(0)
 
                if string_ in "version-history__item__release-date":
                        app_version = tag.string
                        break
 
        except:
                pass
 
 
before_file_path = './tmp/before_date_' + outfile + '.txt'
after_file_path = './tmp/after_date_' + outfile + '.txt'
 
updateTxt(after_file_path)
 
if os.path.exists(before_file_path):
        if not (filecmp.cmp( before_file_path , after_file_path )):
                updateTxt(before_file_path)
                teamsPost()
else:
        updateTxt(before_file_path)