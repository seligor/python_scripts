import os
import urllib.request
from loguru import logger
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import re
import sys
from tqdm import tqdm

logger.remove()
logger.add(sink=sys.stdout, format="<white>{time:YYYY-MM-DD HH:mm:ss}</white>"" | <level>{level: <8}</level>"" | <cyan><b>{line}</b></cyan>"" - <white><b>{message}</b></white>")
logger = logger.opt(colors=True)

workfolder = os.getcwd() + '\\'

# укажите папку, куда должны складываться дистрибутивы
distr = 'E:\\distr\\OS\\linux\\'

def debian():
    distrdir = distr + 'debian\\'
    if not os.path.exists(distrdir):
        os.makedirs(distrdir)
    url = 'https://cdimage.debian.org/debian-cd/current/amd64/iso-dvd/'
    with urllib.request.urlopen(url) as response:
        content = response.read().decode('utf-8')
    pattern = re.compile(
        r'<tr class="odd">.*?<td class="indexcolname"><a href="(debian.*\.iso)">.*<td class="indexcollastmod">(\d{4}-\d{2}-\d{2})\s(\d{2}:\d{2}).*</td></tr>',
        re.DOTALL
    )

    matches = pattern.findall(content)

    if matches:
        iso = matches[-1][0]
        logger.info('Скачивается дистрибутив Debian')
        download(distrdir, url, iso)
    else:
        logger.error("Не удалось обнаружить ссылку на дистрибутив")


def ubuntu():
    distrdir = distr + 'ubuntu\\'
    if not os.path.exists(distrdir):
        os.makedirs(distrdir)
    url = 'https://releases.ubuntu.com/'
    with urllib.request.urlopen(url) as response:
        content = response.read().decode('utf-8')
#    versions = []   #создаём массив, куда поместим все доступные версии для скачивания
    pattern = re.compile(
        r'">([12][24680].04.\d{1,2})/</a>|([12][24680]\.04)/</a>', re.DOTALL)

    versions = pattern.findall(content)
    versions = list(set(versions))
    versions.sort()
    if versions[-1][0]:
        latest_version = versions[-1][0]
    elif versions[-1][1]:
        latest_version = versions[-1][1]
    else:
        logger.error(f'Не удалось обнаружить версию')
        return
    latest_url = f'https://releases.ubuntu.com/{latest_version}/'
    with urllib.request.urlopen(latest_url) as response:
        content = response.read().decode('utf-8')
    iso_pattern = re.compile(
        r'</td><td><a.*?(ubuntu-' + latest_version + '-desktop-amd64.iso)</a>')
    matches = iso_pattern.findall(content)
    if matches:
        iso = matches[-1]
        url = latest_url
        logger.info('Скачивается дистрибутив Ubuntu')
        download(distrdir, url, iso)
    else:
        logger.error("Не удалось обнаружить ссылку на дистрибутив")


def fedora():
    distrdir = distr + 'fedora\\'
    if not os.path.exists(distrdir):
        os.makedirs(distrdir)
    url = 'https://fedoraproject.org/workstation/download/'
    with urllib.request.urlopen(url) as response:
        content = response.read().decode('utf-8')
    pattern = re.compile(
        r'((https://download\.fedoraproject\.org.*/)(Fedora-Workstation-Live-x86_64-(\d{2})[-.\d]{3,6}\.iso))')
    matches = pattern.findall(content)
    if matches:
        last_match = matches[-1]
        iso_url = last_match[0]
        addr, iso = os.path.split(iso_url)
        addr = addr + "/"
        logger.info('Скачивается дистрибутив Fedora')
        download(distrdir, addr, iso)

def redos():
    distrdir = distr + 'redos\\'
    if not os.path.exists(distrdir):
        os.makedirs(distrdir)
    url = 'https://redos.red-soft.ru/product/downloads/'
    with urllib.request.urlopen(url) as response:
        content = response.read().decode('utf-8')
    pattern = re.compile(
        r'<a href="(https://files\.red-soft\.ru/redos/8\.\d{1,2}/x86_64/iso/)(redos[-\w.]{18,28}-x86_64-DVD1\.iso)" target="_blank" class="downloads-files__item-value">')
    matches = pattern.findall(content)
    if matches:
        last_match = matches[-1]
        addr = last_match[0]
        iso = last_match[1]
        logger.info('Скачивается дистрибутив Redos')
        download(distrdir, addr, iso)

def alt():
    distrdir = distr + 'alt\\'
    if not os.path.exists(distrdir):
        os.makedirs(distrdir)
    url = 'https://www.basealt.ru/alt-workstation/download/'
    with urllib.request.urlopen(url) as response:
        content = response.read().decode('utf-8')
    pattern = re.compile(
        r'href="(https://download.basealt.ru/pub/distributions/ALTLinux/(p\d+)/images/workstation/x86_64/)(alt-workstation-(\d{1,2}\.\d+)-x86_64.iso)"')
    matches = pattern.findall(content)
    if matches:
        last_match = matches[-1]
        addr = last_match[0]
        iso = last_match[2]
        url = addr + '/'
        logger.info('Скачивается дистрибутив Altlinux desktop')
        download(distrdir, url, iso)

def altserver():
    distrdir = distr + 'alt\\'
    if not os.path.exists(distrdir):
        os.makedirs(distrdir)
    url = 'https://www.basealt.ru/alt-server/download'
    with urllib.request.urlopen(url) as response:
        content = response.read().decode('utf-8')
    pattern = re.compile(
        r'href="(https://download.basealt.ru/pub/distributions/ALTLinux/(p\d+)/images/server/x86_64/)(alt-server-(\d{1,2}\.\d+)-x86_64.iso)"')
    matches = pattern.findall(content)
    if matches:
        last_match = matches[0]
        addr = last_match[0]
        iso = last_match[2]
        logger.info('Скачивается дистрибутив AltServer')
        download(distrdir, addr, iso)


def centos():
    distrdir = distr + 'centos\\'
    if not os.path.exists(distrdir):
        os.makedirs(distrdir)
    url = 'https://www.centos.org/download/'
    with urllib.request.urlopen(url) as response:
        content = response.read().decode('utf-8')
    pattern = re.compile(
        r'href="(https://mirrors\.centos\.org/mirrorlist\?path=/(\d+)-stream/BaseOS/x86_64/iso/(CentOS-Stream-(\d+)-latest-x86_64-dvd1.iso)&amp;redirect=1&amp;protocol=https)">')
    matches = pattern.findall(content)
    if matches:
        last_match = matches[0]
        addr = last_match[0]
        iso = last_match[2]
        with urllib.request.urlopen(addr) as response:
            content = response.read().decode('utf-8')
        pattern = re.compile(r'(http://[\w.\-]+\.ru/[\w.\-/]+/x86_64/iso/)'+iso)
        matches = pattern.findall(content)
        if matches:
            addr = matches[0]
            logger.info('Скачивается дистрибутив Centos')
            download(distrdir, addr, iso)


def alma():
    distrdir = distr + 'alma\\'
    if not os.path.exists(distrdir):
        os.makedirs(distrdir)
    url = 'https://almalinux.org/get-almalinux/'
    request = urllib.request.Request(url)
    request.add_header('Accept', 'text/html')
    request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15' )
    with urllib.request.urlopen(request) as response:
        content = response.read().decode('utf-8')
    pattern = re.compile(
        r'<a href=(https://repo.almalinux.org/almalinux/)(\d+\.\d+)(/isos/x86_64/)(AlmaLinux-)(\d+\.\d+)(-x86_64-dvd\.iso)>[\w.\s]+</a>')
    matches = pattern.findall(content)
    if matches:
        last_match = matches[0]
        addr = last_match[0]+last_match[1]+last_match[2]
        iso = last_match[3]+last_match[4]+last_match[5]
        logger.info('Скачивается дистрибутив AlmaLinux')
        download(distrdir, addr, iso)


def download(distrdir, url, iso):
    try:
        if os.path.exists(os.path.join(distrdir, iso)):
            logger.error(f'Файл {os.path.join(distrdir, iso)} уже существует')
            return

        logger.info(
            f'Идёт скачивание новой версии. По окончании скачивания появится файл {os.path.join(distrdir, iso)}')

        response = requests.get(url + iso, verify=False, stream=True)
        response.raise_for_status()  # Raise an error for bad responses

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # Size of each chunk we will write
        with open(os.path.join(distrdir, iso), 'wb') as f:
            # Initialize tqdm progress bar
            with tqdm(total=total_size, unit='iB', unit_scale=True) as progress_bar:
                for data in response.iter_content(block_size):
                    f.write(data)
                    progress_bar.update(len(data))

        logger.success(f'Файл успешно скачан')

    except requests.exceptions.RequestException as e:
        logger.error(f'Ошибка скачивания файла: {e}')
    except IOError as e:
        logger.error(f'Ошибка при записи файла: {e}')
    except KeyboardInterrupt:
        logger.warning('Скачивание было прервано пользователем')


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
              """)
