from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
import requests
import os


def isDirectory(url):
    if(url.endswith('/')):
        return True
    else:
        return False

file_type=['.tf','.rule']
def findLinks(url):
    page = requests.get(url).content
    bsObj = BeautifulSoup(page, 'html.parser')
    maybe_directories = bsObj.findAll('a', href=True)

    for link in maybe_directories:
        filename=link['href']
        if link['href'].startswith('?') or link['href'].startswith('/'):
            continue
        if(isDirectory(link['href'])):
            print("this is a folder",filename)
            newUrl = url + link['href']   
            print(newUrl)      
            findLinks(newUrl) #recursion happening here
        else:
            print("this is a file",filename)
            pwd=os.getcwd()
            test_url=url.strip('/')
            dirname=os.path.split(test_url)[-1]
            print(dirname)
            if not os.path.exists(pwd+'/'+dirname):
                os.mkdir(pwd+'/'+dirname)
            if(filename.endswith('.tf') or filename.endswith('.rul')) :
                print(url+filename)
                os.chdir(pwd+'/'+dirname)
                r = requests.get(url+filename)
                with open(filename,'wb') as f:
                    f.write(r.content)
                os.chdir(pwd)

startUrl = "https://vlsiarch.ecen.okstate.edu/flows/FreePDK_SRC/techfile/"
findLinks(startUrl)