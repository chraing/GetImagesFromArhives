import requests
from curl_cffi import requests as requests2
from bs4 import BeautifulSoup
import httplib2
import os
from pathlib import Path
import sys
import json
import time


if getattr(sys, 'frozen', False):
    script_path = Path(sys.executable).parent
elif __file__:
    script_path = Path(__file__).parent


print ('Получение изображений со следующих сайтов:\n1. https://cgamos.ru\n2. https://yandex.ru/archive')
katalog = input("Введите URL: ")
katalog=katalog.rstrip()
if katalog[-1:]=='/':
    katalog=katalog[:-1]
print (f'Каталог сохранения изображений {script_path.joinpath(os.path.basename(katalog))}')

if not os.path.isdir(script_path.joinpath(os.path.basename(katalog))):
    dir_new=script_path.joinpath(os.path.basename(katalog))
    os.mkdir(dir_new)
    print (f'Создал каталог {dir_new}')

def GetFromYandexArhive(katalog):
    headers ={
            'Host': 'yandex.ru',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Sec-GPC': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Priority': 'u=0, i',
            'TE': 'trailers',
            'cookie':'is_gdpr=0; is_gdpr_b=CLqxUhDCzgI=; _yasc=2n+giFe48xIWPp0xb0kVYGHs+WQVdcO8oVIFU80XUN47vUkS0YtQRAMMggPLX1Hup3C7+w/+GC7P; i=D1vfCRlPmISzAIXqlxVYlW/vSfyVTRy0v0m5ykZlZNPnbG9Iuj1/UoWLtC8sIXTBJZG3txWsdvsr1voUHLc6H9QmIUM=; yandexuid=5956260211753746309; yashr=7699648801753746309; bh=YO/kosQGahfcyuH/CJLYobEDn8/14Qz01PCOA4vzAg==; yuidss=5956260211753746309; ymex=2069106312.yrts.1753746312; gdpr=0; _ym_uid=1753746312721611344; _ym_d=1753746313; spravka=dD0xNzUzNzQ2MzUzO2k9NzcuODIuMTk0LjE0NTtEPTVCQjQ0Q0JBMDQyNkEyMkRBMDVDQTBGRjI1MjNBODQxQzg4NzMyQThGN0YzNkFFOTAxNEQwNUIxNEIwRUUzRTI3QTY3NjE1QzMyNzQ5QTkzQzNGQkNCRDY0QUNCNEY1MTU2MzBERjk4RDJGRUYwNDk4QTQ2MTAxRDYwNjgyMEEyODg3QTMwNTJCRURCQTVEODkwNzE3OTt1PTE3NTM3NDYzNTM0NDkwNjQ4MzA7aD1kYjhlNmJmNDI0ZWUyOGUyNTM0ZTY4YmU2MmMyM2I2Ng==; _ym_isad=2; _ym_visorc=w'
    } 
    cookies={
            "_yasc": "2n+giFe48xIWPp0xb0kVYGHs+WQVdcO8oVIFU80XUN47vUkS0YtQRAMMggPLX1Hup3C7+w/+GC7P",
            "_ym_d": "1753746313",
            "_ym_isad": "2",
            "_ym_uid": "1753746312721611344",
            "_ym_visorc": "w",
            "bh": "YO/kosQGahfcyuH/CJLYobEDn8/14Qz01PCOA4vzAg==",
            "gdpr": "0",
            "i": "D1vfCRlPmISzAIXqlxVYlW/vSfyVTRy0v0m5ykZlZNPnbG9Iuj1/UoWLtC8sIXTBJZG3txWsdvsr1voUHLc6H9QmIUM=",
            "is_gdpr": "0",
            "is_gdpr_b": "CLqxUhDCzgI=",
            "spravka": "dD0xNzUzNzQ2MzUzO2k9NzcuODIuMTk0LjE0NTtEPTVCQjQ0Q0JBMDQyNkEyMkRBMDVDQTBGRjI1MjNBODQxQzg4NzMyQThGN0YzNkFFOTAxNEQwNUIxNEIwRUUzRTI3QTY3NjE1QzMyNzQ5QTkzQzNGQkNCRDY0QUNCNEY1MTU2MzBERjk4RDJGRUYwNDk4QTQ2MTAxRDYwNjgyMEEyODg3QTMwNTJCRURCQTVEODkwNzE3OTt1PTE3NTM3NDYzNTM0NDkwNjQ4MzA7aD1kYjhlNmJmNDI0ZWUyOGUyNTM0ZTY4YmU2MmMyM2I2Ng==",
            "yandexuid": "5956260211753746309",
            "yashr": "7699648801753746309",
            "ymex": "2069106312.yrts.1753746312",
            "yuidss": "5956260211753746309"
    }  
    s = requests2.Session()
    s.headers = headers
    s.cookies= cookies
    cur_page='?pageNum=1'
    urls_image_opisey=[]
    while cur_page:
        url_documenta=f'{katalog}{cur_page}'
        response = s.get(url_documenta)
        print (f'Запрос на {url_documenta}')
        bs = BeautifulSoup(response.text,"html.parser")

        temp = bs.find('script', type='application/json')
        if temp is not None:
            temp=temp.text
        else:
            err=bs.find_all('div', class_='Spacer')
            print (err[1].text)
            break
        next_page=bs.find('a', class_='Pagination-PagesItem Pagination-PagesNext')
        
        if next_page is not None:
            cur_page=next_page.get('href')
        else:
            cur_page=False
   
        python_object = json.loads(str(temp))
        childNodes=python_object['props']['pageProps']['childNodes']
        if childNodes  is not None:
            for nod in childNodes:
                if nod is not None and nod.get('thumb',False):
                    img='https://yandex.ru'+str(nod['thumb']['path']).replace('type=thumb','type=original')
                    urls_image_opisey.append (img)
                else:
                    urls_image_opisey.append ('')
        
    rr_len=len(urls_image_opisey)
    if rr_len>0:
        print (f'Найдено изображений: {rr_len}')
        for i,img in enumerate(urls_image_opisey):
            print (f'{i+1}. {img}')
        start_stop=input("Введите номер (или диапазон) для скачивания изображения (например 10-20 или 11): ")
        if '-' in start_stop:
            start_stop=start_stop.split("-")
        else:
            start_stop=[start_stop,start_stop]

        cnt_dwnload=0
        for i in range(int(start_stop[0])-1,int(start_stop[1])):
            tpm = s.get(f'{katalog}/{i}')
            time.sleep(10)
            if len(urls_image_opisey[i])>1:
                data = s.get(urls_image_opisey[i]) 
                with open(script_path.joinpath(os.path.basename(katalog),str(i+1).zfill(4) +".jpg"), "wb") as out:
                    out.write(data.content)
                cnt_dwnload+=1
            #time.sleep(5)
        print (f'Скачено {cnt_dwnload} изображений.')
    s.close()


def GetFromCgamos(katalog):
    url_documenta=f'{katalog}/'
    headers ={'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.28 Safari/537.36', 'Referer':f'{katalog}/'}   
    s = requests.Session()
    s.headers = headers 
    response = s.get(url_documenta)
    bs = BeautifulSoup(response.text,"lxml")
    temp = bs.find_all('li', class_='swiper-slide')
    urls_image_opisey=[]
    for li in temp:
        urls_image_opisey.append (li.find('img')['data-src'])  
    rr_len=len(temp)
    print (f'Найдено {rr_len} изображений: ')
    #for i,img in enumerate(urls_image_opisey):
    #    print (f'{i+1}. https://cgamos.ru/{img}')
    #Убрано потомучто по прямым сылка не показывает и не качает
    start_stop=input("Введите номер (или диапазон) для скачивания изображения (например 10-20 или 11): ")
    if '-' in start_stop:
        start_stop=start_stop.split("-")
    else:
        start_stop=[start_stop,start_stop]

    cnt_dwnload=0
    if int(start_stop[1])<=rr_len:
        for i in range(int(start_stop[0])-1,int(start_stop[1])):
            data = s.get('https://cgamos.ru'+urls_image_opisey[i]) 
            with open(script_path.joinpath(os.path.basename(katalog),str(i+1).zfill(4) +".jpg"), "wb") as out:
                out.write(data.content)
            cnt_dwnload+=1
    print (f'Скачено {cnt_dwnload} изображений.')
    s.close()

if 'cgamos.ru' in katalog:
    GetFromCgamos(katalog)
elif '/archive/catalog' in katalog:
    GetFromYandexArhive(katalog)

