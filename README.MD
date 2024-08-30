Скрипт скачивания дистрибутивов Linux (можно не ходить по сайтам, просто скачать свежую версию)

для запуска требуетсы выполнить
git clone https://github.com/seligor/python_scripts.git

для ОС Windows
```cmd
python3 -m venv venv
venv/scripts/activate.bat
pip install -r requirements.txt
```
для ОС Linux:
```shell
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Для обоих ОС желательно изменить значение параметра ```distr``` в скрипте для того чтобы загрузка производилась по желаемому пути

При запуске скрипт предложит выбрать какой из дистрибутивов скачивать.
Название дистрибутива принимается в виде аргумента

Например 
```shell
python linux_download.py --debian
```