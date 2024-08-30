Скрипт скачивания дистрибутивов Linux (можно не ходить по сайтам, просто скачать свежую версию)

для запуска требуетсы выполнить
git clone https://github.com/seligor/python_scripts.git
```shell
python3 -m venv venv
venv/scripts/activate.bat
pip install -r requirements.txt
python linux_download.py
```
При запуске скрипт предложит выбрать какой из дистрибутивов скачивать.
Название дистрибутива принимается в виде аргумента

Например 
```shell
python linux_download.py --debian
```