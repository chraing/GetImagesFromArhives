import requests
from curl_cffi import requests as requests2
from bs4 import BeautifulSoup
import httplib2
import os
from pathlib import Path
import sys
import json
import time
import threading
import  settings
import re


def _init(katalog):
    lock = threading.Lock()
    katalog=katalog.rstrip()
    if katalog[-1:]=='/':
        katalog=katalog[:-1]
    if getattr(sys, 'frozen', False):
        script_path = Path(sys.executable).parent
    elif __file__:
        script_path = Path(__file__).parent
    dir_new=script_path.joinpath('uploaded_images',os.path.basename(katalog))
    #print ('dir_new',dir_new)
    if not os.path.isdir(dir_new):    
        print ('Создаю каталог',dir_new)
        os.mkdir(dir_new) 
    return lock,katalog,dir_new

def _save_images(urls,lock,number_trs,sess,dir_new,start,stop,pref_url,sleep_mls):
    rr_len=len(urls)
    with lock:  
        settings.trs[number_trs]['count_rec']=rr_len
    print (f'Найдено {rr_len} изображений: ')
    if  start=='':
        start=1
    if  stop=='':
        stop=rr_len
    if int(start)<=rr_len:
        settings.trs[number_trs]['status']='0'
        for i in range(int(start)-1,int(stop)):
            data = sess.get(pref_url+urls[i],cookies)
            while len(data.text)<50000:
                data = sess.get(pref_url+urls[i],cookies)

            time.sleep(sleep_mls) 
            with open(dir_new.joinpath(str(i+1).zfill(4) +".jpg"), "wb") as out:
                out.write(data.content)
            with lock:    
                settings.trs[number_trs]['status']=int(settings.trs[number_trs]['status'])+1
    

def GetFromTula(katalog,start,stop,number_trs,login,password):    
    lock,katalog,dir_new=_init(katalog)  
    s = requests.Session()
    # Ниже данные для авторизации
    payload = {
        'username': login,
        'password': password
        }
    url_documenta='https://gato.tularegion.ru/case/'+katalog #Контретный документ который грузим (посмотреть )
    headers = {'Content-Type': 'application/json','User-Agent':	'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0'}
    response = s.get('https://gato.tularegion.ru/login')
    response = s.post('https://gato.tularegion.ru/auth',headers=headers, json=payload)
    bearer=response.json()['token']
    response = s.get(url_documenta) 
    bs = BeautifulSoup(response.text,"lxml")
    temp = bs.find('a', 'btn case-tile-button btn-secondary read')
    if temp is None:
        return number_trs,"Проверьте, активна ли подписка на сайте архива"
    else:
        ssilka=temp['href']
        response = s.get('https://gato.tularegion.ru/lksrv'+ssilka,cookies={'auth.strategy':'local','auth._token.local':bearer})
        print ('https://gato.tularegion.ru/lksrv'+ssilka)
        soup = BeautifulSoup(response.text, "html.parser")
        scriptt = soup.find("script")
        r0=re.search(r'checkRequiredPayment\(img, (\w{30})',str(scriptt),flags=re.MULTILINE| re.DOTALL).group(1); #тут нужный ключ
        print(katalog,'Нашел ключ с изображениями')
        rr=re.search('var '+r0+' = \[(.*?)\]', str(scriptt),flags=re.MULTILINE| re.DOTALL).group(1)
        rr=rr.replace("'","")
        rr=rr.split(", ")
        _save_images(rr,lock,number_trs,s,dir_new,start,stop,'https://gato.tularegion.ru/lksrv/private/imageViewer/image?url=',0,{'auth.strategy':'local','auth._token.local':bearer})
    s.close()
    return number_trs,None


def GetFromKaluga(katalog,start,stop,number_trs,login,password):
    lock,katalog,dir_new=_init(katalog)            
    s = requests.Session()
    payload = {
        'backURL': 'https://archive.admoblkaluga.ru/login',
        'username': login,
        'password': password
        }
    url_documenta='https://archive.admoblkaluga.ru/private/office/documents?oid='+katalog #Контретный документ который грузим (посмотреть )
    response = s.post('https://archive.admoblkaluga.ru/login', data=payload)
    response = s.get(url_documenta) 
    bs = BeautifulSoup(response.text,"lxml")
    temp = bs.find('a', 'btn btn-primary btn-kaisa-action')
    if temp is None:
        return number_trs,"Проверьте, активность подписки и логин/пароль"
    else:
        ssilka=temp['href']
        response = s.get('https://archive.admoblkaluga.ru'+ssilka)
        soup = BeautifulSoup(response.text, "html.parser")
        scriptt = soup.find("script")
        r0=re.search(r'checkRequiredPayment\(img, (\w{30})',str(scriptt),flags=re.MULTILINE| re.DOTALL).group(1); #тут нужный ключ
        print(katalog,'Нашел ключ с изображениями')
        rr=re.search('var '+r0+' = \[(.*?)\]', str(scriptt),flags=re.MULTILINE| re.DOTALL).group(1)
        rr=rr.replace("'","")
        rr=rr.split(", ")
        _save_images(rr,lock,number_trs,s,dir_new,start,stop,'https://archive.admoblkaluga.ru/private/imageViewer/image?url=',0,None)
    s.close()
    return number_trs,None
    

def GetFromCgamos(katalog,start,stop,number_trs,login,password):   
    lock,katalog,dir_new=_init(katalog)
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
    _save_images(urls_image_opisey,lock,number_trs,s,dir_new,start,stop,'https://cgamos.ru',0,None)
    s.close()
    return number_trs,None


def GetFromYandexArhive(katalog,start,stop,number_trs,login,password):
    lock,katalog,dir_new=_init(katalog)
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
        
    _save_images(urls_image_opisey,lock,number_trs,s,dir_new,start,stop,'',10,None)
    s.close()
    return number_trs,None