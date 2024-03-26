import os
import urllib.request
#import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import re
import requests
from urllib.parse import urlencode
import sys
workfolder = os.getcwd() + '\\'

# укажите папку, куда должны складываться дистрибутивы
distr = 'E:\\distr\\OS\\linux\\'

def debian():
    distrdir = distr + '\\debian\\'
    if not os.path.exists(distrdir):
        os.makedirs(distrdir)
    url = 'https://cdimage.debian.org/debian-cd/current/amd64/iso-dvd/'
    page = urllib.request.urlopen(url)
    content = page.read()
    f = open("data.req", "w")
    f.write(str(content))
    f.close()
    f=open(workfolder + r'data.req',"r")
    pattern = re.compile('\<tr class\=\"odd\"\>.*?\<td class\=\"indexcolname\"\>\<a href\=\"(debian.*\.iso)\"\>.*\<td class\=\"indexcollastmod\"\>(\d{4}\-\d{2}\-\d{2})\s(\d{2}\:\d{2}).*\<\/td\>\<\/tr\>')
    for i, line in enumerate(open(workfolder + 'data.req')):
        for match in re.finditer(pattern, line):
            dateexpire = str(match.group(2))
            iso = str(match.group(1))
    f.close()
    os.remove('data.req')
    download(distrdir, url, iso)


def ubuntu():
    distrdir = distr + '\\ubuntu\\'
    if not os.path.exists(distrdir):
        os.makedirs(distrdir)
    url = 'https://releases.ubuntu.com/'
    page = urllib.request.urlopen(url)
    content = page.read()
    f = open("data.req", "w")
    f.write(str(content))
    f.close()
    versions = []   #создаём массив, куда поместим все доступные версии для скачивания
    f=open(workfolder + r'data.req',"r")
    pattern = re.compile('">([12][2,4,6,8,0]\.04\.\d{1,2})\/<\/a>|([12][2,4,6,8,0]\.04)\/<\/a>')
    for i, line in enumerate(open(workfolder + 'data.req')):
        for match in re.finditer(pattern, line):
            version2 = str(match.group(1)) # для версий из 2 чисел
            version3 = str(match.group(2)) #для версий из 3 чисел
            versions.append(version2)
            versions.append(version3)
            versions.remove('None')
    versions.sort() # сортирую массив, чтобы получить самую последнюю доступную версию
    f.close()
    url = 'https://releases.ubuntu.com/'+ versions[-1] + '/' #самвя свежая версия
    page = urllib.request.urlopen(url)
    content = page.read()
    f = open("data2.req", "w")
    f.write(str(content))
    f.close()
    f=open(workfolder + r'data2.req',"r")
    pattern = re.compile('<\/td><td><a.*?(ubuntu-' + versions[-1] + '-desktop-amd64\.iso)<\/a>')
    for i, line in enumerate(open(workfolder + 'data2.req')):
        for match in re.finditer(pattern, line):
            iso = str(match.group(1))
            url = 'https://releases.ubuntu.com/' + versions[-1] + '/'
    f.close()
    os.remove('data2.req')
    os.remove('data.req')
    download(distrdir, url, iso)

def fedora():
    distrdir = distr + '\\fedora\\'
    if not os.path.exists(distrdir):
        os.makedirs(distrdir)
    url = 'https://fedoraproject.org/workstation/download/'
    page = urllib.request.urlopen(url)
    content = page.read()
    f = open("data.req", "w")
    f.write(str(content))
    f.close()
    f=open(workfolder + r'data.req',"r")
    pattern = re.compile('((https:\/\/download\.fedoraproject\.org.*\/)(Fedora-Workstation\-Live\-x86\_64\-(\d{2})[-\.\d]{3,6}\.iso))')
    for i, line in enumerate(open(workfolder + 'data.req')):
        for match in re.finditer(pattern, line):
            url = str(match.group(2))
            iso = str(match.group(3))
    f.close()
    os.remove('data.req')
    download(distrdir, url, iso)


def download(distrdir, url, iso):
    if os.path.exists(distrdir + iso):
        print(r'Файл ' + distrdir + iso + r' уже существует')
    else:
        print(r'Идёт скачивание новой версии. По окончании скачивания появится файл '+ distrdir + iso)
        f=open(distrdir + iso,"wb")
        ufr = requests.get(url + iso, verify=False, stream=True)
        for chunk in ufr.iter_content(chunk_size=1024): 
            if chunk:
                f.write(chunk)
        f.close()


if __name__ == "__main__":
    if len (sys.argv) > 1:
        if sys.argv[1] == '--debian':
            debian()
        if sys.argv[1] == '--ubuntu':
            ubuntu()
        if sys.argv[1] == '--fedora':
            fedora()
        else:
            print('Неверное указание')
    else:
        print('Напишите название дистрибутива для скачивания. \n Принимаются значения: \n --debian Скачивание дистрибутива debian \n --ubuntu  Скачивание дистрибутива ubuntu \n --fedora Скачивание дистрибутива fedora')
