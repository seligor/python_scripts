import os
import urllib.request
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import re
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

def redos():
    distrdir = distr + '\\redos\\'
    if not os.path.exists(distrdir):
        os.makedirs(distrdir)
    url = 'https://redos.red-soft.ru/product/downloads/'
    page = urllib.request.urlopen(url)
    content = page.read()
    f = open("data.req", "w")
    f.write(str(content))
    f.close()
    f=open(workfolder + r'data.req',"r")
    pattern = re.compile('<a href="(https:\/\/files\.red-soft\.ru\/redos\/8\.\d{1,2}\/x86_64\/iso\/)(redos[-\w\d.]{18,28}-x86_64-DVD1\.iso)" target="_blank" class="downloads-files__item-value">')
    for i, line in enumerate(open(workfolder + 'data.req')):
        for match in re.finditer(pattern, line):
            url = str(match.group(1))
            iso = str(match.group(2))
    f.close()
    os.remove('data.req')
    download(distrdir, url, iso)

def alt():
    distrdir = distr + 'alt\\'
    if not os.path.exists(distrdir):
        os.makedirs(distrdir)
    url = 'https://www.basealt.ru/alt-workstation/download/'
    page = urllib.request.urlopen(url)
    content = page.read()
    f = open("data.req", "w")
    f.write(str(content))
    f.close()
    versions = []
    p = []
    f=open(workfolder + r'data.req',"r")
    pattern = re.compile('href="(https:\/\/download.basealt.ru\/pub\/distributions\/ALTLinux\/(p\d+)\/images\/workstation\/x86_64\/)(alt-workstation-(\d{1,2}\.\d+)\-x86_64.iso)"')
    for i, line in enumerate(open(workfolder + 'data.req')):
        for match in re.finditer(pattern, line):
            url = str(match.group(1))
            vp = str(match.group(2))
            p.append(vp)
            p.sort(reverse=True)
            version = str(match.group(4))
            versions.append(version)
            versions.sort(reverse=True)
            url = 'https://download.basealt.ru/pub/distributions/ALTLinux/'+p[-1]+'/images/workstation/x86_64/'
            iso = 'alt-workstation-'+versions[-1]+'-x86_64.iso'
    f.close()
    os.remove('data.req')
    download(distrdir, url, iso)

def altserver():
    distrdir = distr + 'alt\\'
    if not os.path.exists(distrdir):
        os.makedirs(distrdir)
    url = 'https://www.basealt.ru/alt-server/download'
    page = urllib.request.urlopen(url)
    content = page.read()
    f = open("data.req", "w")
    f.write(str(content))
    f.close()
    versions = []
    p = []
    f=open(workfolder + r'data.req',"r")
    pattern = re.compile('href="(https:\/\/download.basealt.ru\/pub\/distributions\/ALTLinux\/(p\d+)\/images\/server\/x86_64\/)(alt-server-(\d{1,2}\.\d+)\-x86_64.iso)"')
    for i, line in enumerate(open(workfolder + 'data.req')):
        for match in re.finditer(pattern, line):
            url = str(match.group(1))
            vp = str(match.group(2))
            p.append(vp)
            p.sort(reverse=True)
            version = str(match.group(4))
            versions.append(version)
            versions.sort(reverse=True)
            url = 'https://download.basealt.ru/pub/distributions/ALTLinux/'+p[-1]+'/images/server/x86_64/'
            iso = 'alt-server-'+versions[-1]+'-x86_64.iso'
    f.close()
    os.remove('data.req')
    download(distrdir, url, iso)

def centos():
    distrdir = distr + 'centos\\'
    if not os.path.exists(distrdir):
        os.makedirs(distrdir)
    url = 'https://www.centos.org/download/'
    page = urllib.request.urlopen(url)
    content = page.read()
    f = open("data.req", "w")
    f.write(str(content))
    f.close()
    versions = []
    f=open(workfolder + r'data.req',"r")
    pattern = re.compile('href="(https:\/\/mirrors\.centos\.org\/mirrorlist\?path=\/(\d+)-stream\/BaseOS\/x86_64\/iso\/(CentOS-Stream-(\d+)-latest-x86_64-dvd1.iso)&amp;redirect=1&amp;protocol=https)">')
    for i, line in enumerate(open(workfolder + 'data.req')):
        for match in re.finditer(pattern, line):
            url1 = str(match.group(1))
            iso = str(match.group(3))
            page = urllib.request.urlopen(url1)
            content = page.read()
            f = open("data2.req", "w")
            f.write(str(content))
            f.close()
            f=open(workfolder + r'data2.req',"r")
            pattern = re.compile('(http:\/\/[\w.\-]+\.ru\/[\w\.\-\/]+\/x86_64\/iso\/)'+iso)
            for i, line in enumerate(open(workfolder + 'data2.req')):
                for match in re.finditer(pattern, line):
                    url= str(match.group(1))
            f.close()
    f.close()
    os.remove('data.req')
    os.remove('data2.req')
    download(distrdir, url, iso)

def alma():
    distrdir = distr + '\\alma\\'
    if not os.path.exists(distrdir):
        os.makedirs(distrdir)
    url = 'https://almalinux.org/get-almalinux/'
    st_accept = "text/html" # говорим веб-серверу, 
                            # что хотим получить html. Ибо обычные запросы алма почему то 403 делает. Притворяемся брвузером
    st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
    headers = {
       "Accept": st_accept,
       "User-Agent": st_useragent
    }
    req = requests.get("https://almalinux.org/get-almalinux/", headers)
    # считываем текст HTML-документа
    content = req.text
    f = open("data.req", "w", encoding="UTF-8")
    f.write(str(content))
    f.close()
    versions = []   #создаём массив, куда поместим все доступные версии для скачивания
    f=open(workfolder + r'data.req',"r")
    pattern = re.compile('<a href=(https:\/\/repo.almalinux.org\/almalinux\/)(\d+\.\d+)(\/isos\/x86_64\/)(AlmaLinux\-)(\d+\.\d+)(\-x86_64\-dvd\.iso)>[\w\.\s]+<\/a>')
    for i, line in enumerate(open(workfolder + 'data.req')):
        for match in re.finditer(pattern, line):
            version = str(match.group(2)) # для версий из 2 чисел
            versions.append(version)
    versions.sort() # сортирую массив, чтобы получить самую последнюю доступную версию
    f.close()
    version = versions[-1]
    url = str(match.group(1))+version+str(match.group(3))
    iso = str(match.group(4))+version+str(match.group(6))
    os.remove('data.req')
    download(distrdir, url, iso)


def alllinux():
    ubuntu()
    debian()
    fedora()
#    rosa() 
#    astra()
    centos()
#    redhat()
    alma()
    alt()
    altserver()
    redos()

def download(distrdir, url, iso):
    print(url)
    print(iso)
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
        elif sys.argv[1] == '--ubuntu':
            ubuntu()
        elif sys.argv[1] == '--fedora':
            fedora()
        elif sys.argv[1] == '--redos':
            redos()
        elif sys.argv[1] == '--alt':
            alt()
        elif sys.argv[1] == '--altserver':
            altserver()
        elif sys.argv[1] == '--centos':
            centos()
        elif sys.argv[1] == '--alma':
            alma()
        elif sys.argv[1] == '--alllinux':
            alllinux()
        else:
            print('Неверное указание (такой ОС нет в списке принимаемых аргументов)', sys.argv[1])
    else:
        print("""\n\nНапишите название дистрибутива для скачивания.

                 Принимаются значения:
                 --debian Скачивание дистрибутива debian
                 --ubuntu  Скачивание дистрибутива ubuntu
                 --fedora Скачивание дистрибутива fedora
                 --redos Скачивание дистрибутива redos
                 --alt Скачивание дистрибутива ALTLiniux
                 --altserver Скачивание дистрибутива ALTLinux server
                 --centos Скачивание дистрибутива CentOS
                 --alma Скачивание дистрибутива AlmaLinux
                 --alllinux Скачивание всех дистрибутивов (44.8 ГБ)
              """)
